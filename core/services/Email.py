from dotenv import load_dotenv
import os
from ..middlewares import mailjet

load_dotenv()
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")


async def send_email(message_data: dict):
    data = {
        "Messages": [
            {
                "From": {
                    "Email": SENDER_EMAIL,
                    "Name": "No Budget Shop"
                },
                "To": message_data["to"],
                "Subject": message_data["subject"],
                "TextPart": message_data["TextPart"],
                "HTMLPart": message_data["HTMLPart"]
            }
        ]
    }

    result = mailjet.client.send.create(data=data)
    return result.status_code
