import datetime as dt 
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from twilio.rest import Client
import openai

from rasa_sdk.events import UserUtteranceReverted

openai.api_key = "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"

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"{dt.datetime.now()}")

        return []
    
class VSrec(Action):
    def name(self) -> Text:
        return "action_vs_rec"

    def run(self, dispatcher, tracker, domain):
        
        ques = tracker.latest_message.get("text")
        location = tracker.get_slot("location")
        bodysize = tracker.get_slot("bodytype")
        specifics = tracker.get_slot("specifics")
        age = tracker.get_slot("age")
        sex = tracker.get_slot("gender")
        occasion =  tracker.get_slot("occasion")

        if specifics == "no" or "NO" or "No":

            completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": f'you are a fashion assistant who takes into account "{age}""{sex}"body size"{bodysize}""{occasion}""{location}" and suggest clothes , lingiere, accessories and footwear possibally from "Victoria secret"'},
                ]
            )

            

            if len(completion.choices) > 0:

                 response = completion['choices'][0]['message']['content']
            else:
                response = "Sorry, I couldn't understand. Can you please rephrase your query?"

                
                
                

        elif specifics != "no" or "NO" or "No":

            completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": f'you are a fashion assistant who takes into account "{age}""{sex}"body size"{bodysize}""{occasion}""{location}" and suggest "{specifics}" possibally from "Victoria secret"'},
                ]
            )

            if len(completion.choices) > 0:

                 response = completion['choices'][0]['message']['content']
            else:
                response = "Sorry, I couldn't understand. Can you please rephrase your query?"
        
            
        
           

        dispatcher.utter_message(response)

        return [UserUtteranceReverted()]




class GPTFallbackAction(Action):
    def name(self) -> Text:
        return "action_gpt_fallback"

    def run(self, dispatcher, tracker, domain):
        
        ques = tracker.latest_message.get("text")

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f'you are a fashion assistant created for victoria\'s secret who give response based on input"{ques}"'},
            ]
        )

        if len(completion.choices) > 0:
            response = completion['choices'][0]['message']['content']
        else:
            response = "Sorry, I couldn't understand. Can you please rephrase your query?"

        dispatcher.utter_message(response)

        return [UserUtteranceReverted()]


class SendSMS(Action):
    def name(self) -> Text:
        return "action_send_alert_sms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Set up the Twilio client
        account_sid = 'AC681fb0cc44dc4e70d2e53f599b71de72'
        auth_token = '36f64077cdafac367e05bfb7160042a1'
        client = Client(account_sid, auth_token)

        # Define the recipient's phone number and the message
        recipient_number = '+918851251407' # Replace with the phone number you want to send the message to
        message_body = 'ALERT: Your Patient looks uncomfortable -sent from alzhistant'

        # Use the Twilio API to send the message
        message = client.messages.create(
            body=message_body,
            from_='<+15074287641>', # Replace with your Twilio phone number
            to=recipient_number
        )

        # Send a response message to the user
        dispatcher.utter_message(text="SMS notification sent!")

        return []
