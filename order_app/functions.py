from __future__ import print_function

import africastalking

class SMS:
    def __init__(self):
        self.username = "urimltd"
        self.api_key = (
            "a8daea4353fe3345a913fc34cc777df018cd3e5f52555ad9fac800360db3cdba"
        )

        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)

        # Get the SMS service
        self.sms = africastalking.SMS

    def send(self, message, recipient):
        recipients = [recipient]
        sender = ""

        try:
            response = self.sms.send(message, recipients)
            print(response)
        except Exception as e:
            print("Encountered an error while sending: %s" % str(e))


sms_service = SMS()


# why this error

# {'SMSMessageData': {'Message': 'Sent to 0/1 Total Cost: 0', 'Recipients': [{'cost': '0', 'messageId': 'None', 'number': '+254790780464', 'status': 'UserInBlacklist', 'statusCode': 406}]}}
