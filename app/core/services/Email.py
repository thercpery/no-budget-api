from ..middlewares import mailjet


async def send_email(message_data: dict):
    data = {
        "Messages": [
            {
                "From": {
                    "Email": "sarsicoola@gmail.com",
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
