import os
import boto3
import openai

# Retrieve variables from AWS DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('your-dynamodb-table-name')
response = table.get_item(Key={'id': 'your-item-id'})
item = response['Item']
age = item['age']
sex = item['sex']
bodysize = item['bodysize']
country = item['country']

# Prompt the user for the occasion of their outfit
occasion = input("Please tell us the occasion of your outfit: ")

# Call OpenAI GPT-3 API to get a response
openai.api_key = "your-openai-api-key"
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": f'you are a fashion assistant who takes into account "{age}""{sex}"body size"{bodysize}""{occasion}""{country}" and suggest clothes , lingiere, accessories and footwear possibally from "Victoria secret"'},
  ]
)
ans=completion['choices'][0]['message']['content']
print(ans)
