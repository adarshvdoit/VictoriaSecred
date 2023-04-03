# Import the required libraries
from twilio.rest import Client

# Set up the Twilio credentials
account_sid = 'AC681fb0cc44dc4e70d2e53f599b71de72'
auth_token = '36f64077cdafac367e05bfb7160042a1'
client = Client(account_sid, auth_token)

# Define the recipient's phone number and the message
recipient_number = '+9188104 21579' # Replace with the phone number you want to send the message to
message_body = 'ALERT: Your Patient looks uncomfortable -sent from alzhistant'

# Use the Twilio API to send the message
message = client.messages.create(
    body=message_body,
    from_='<+15074287641>', # Replace with your Twilio phone number
    to=recipient_number
)

# Print the message SID as confirmation
print(f"Message sent successfully! SID: {message.sid}")
