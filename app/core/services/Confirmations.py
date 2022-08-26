from dotenv import load_dotenv
import os
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from ..middlewares import database
from ..models.Confirmation import Confirmation
from . import Email

load_dotenv()
BASE_URL = os.environ.get("BASE_URL")

confirmations_collection = database.confirmations_collection
users_collection = database.users_collection


async def send_confirmation_email(user_obj: dict):
    confirmation_obj = Confirmation(userId=user_obj["_id"])
    confirmation_data = jsonable_encoder(confirmation_obj)
    new_confirmation_obj = confirmations_collection.insert_one(confirmation_data)
    new_confirmation_data = confirmations_collection.find_one({"_id": new_confirmation_obj.inserted_id})

    message_data = {
        "to": [
            {
                "Email": user_obj["email"],
                "Name": user_obj["username"]
            }
        ],
        "subject": "Account confirmation",
        "TextPart": "Greetings! You have to confirm your email by clicking on the link.",
        "HTMLPart": f"""<h3>Hi, {user_obj['username']}!</h3>
<br>
<p>You have to confirm your account by clicking on the link <a href='{BASE_URL}/{new_confirmation_data["_id"]}'>here.</a> Please take note that the link only last for <strong>30 minutes.</strong> </p>
<br>
Click on the link below if the link does not work.
{BASE_URL}/{new_confirmation_data["_id"]}
        """
    }

    return await Email.send_email(message_data=message_data)


async def confirm_user(_id: str):
    confirmation_data = confirmations_collection.find_one({"_id": _id})
    user_data = users_collection.find_one({"_id": confirmation_data["userId"]})

    if \
            (confirmation_data is None) or \
            (confirmation_data["isConfirmed"]):
        return False

    if datetime.utcnow() > datetime.strptime(confirmation_data["expireAt"], "%Y-%m-%dT%H:%M:%S.%f"):
        await send_confirmation_email(user_obj=user_data)
        return False

    confirmation_data["isConfirmed"] = True
    confirmation_data["dateUpdated"] = datetime.now()
    user_data["isConfirmed"] = True
    user_data["dateUpdated"] = confirmation_data["dateUpdated"]

    confirmations_collection.update_one({"_id": confirmation_data["_id"]}, {"$set": confirmation_data})
    users_collection.update_one({"_id": user_data["_id"]}, {"$set": user_data})

    message_data = {
        "to": [
            {
                "Email": user_data["email"],
                "Name": user_data["username"]
            }
        ],
        "subject": "Account successfully confirmed!",
        "TextPart": "Congrats! You can now shop without any budget whatsoever!",
        "HTMLPart": f"""<h3>Hi, {user_data['username']}!</h3>
        <p><strong>Congratulations!</strong> You can now shop without any budget whatsoever!</p>
        """
    }

    await Email.send_email(message_data=message_data)

    return True


