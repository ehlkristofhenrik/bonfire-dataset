from itertools import chain
import os
from groq import Groq
import pandas as pd
import json

# class SecuScore:
#     overall_reasoning: str
#     malignity_reasoning: str
#     malignity_score: int
#     severity_reasoning: str
#     severity_score: int
#     utility_reasoning: str
#     utility_score: int
#     expectance_reasoning: str
#     expectance_score: int

system_prompt = ""
with open("../static/system_prompt.txt", "r") as system_prompt_txt:
    system_prompt = system_prompt_txt.read()


client = Groq(
    api_key=os.environ.get('GROQ_API_KEY'),
)

df = pd.read_json("dataset.json")

output = []

for i, o, index in zip(df['input'], df['output'], range(len(df["input"]))):
    for c in o['ethical_hackers']:
        resp = client.chat.completions.create(
        model="llama-3.2-1b-preview",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": "Give your response in JSON! Please analyze: " + str({
                    "user": i['user'],
                    "task": i['task'],
                    "role": i['role'],
                    "command": c
                }),
            }
        ]
        )

        resp = resp.choices[0].message.content
        resp = resp[resp.find("{"):resp.rfind("}")+1]

        try:
            jason = json.loads(resp)
            result = {
                "expected_result": "attacker",
                "task_id": index,
                "task": i['task'],
                "role": i['role'],
                "user": i['user'],
                "command": c,
                "malignity_score": jason['malignity_score'],
                "severity_score": jason['severity_score'],
                "utility_score": jason['utility_score'],
                "expectance_score": jason['expectance_score']
            }
            print(json.dumps(result), ",")
        except:
            ...
    for c in o['legitimate_users']:
        resp = client.chat.completions.create(
        model="llama-3.2-1b-preview",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": "Give your response in JSON! Please analyze: " + str({
                    "user": i['user'],
                    "task": i['task'],
                    "role": i['role'],
                    "command": c
                }),
            }
        ]
        )

        resp = resp.choices[0].message.content
        resp = resp[resp.find("{"):resp.rfind("}")+1]

        try:
            jason = json.loads(resp)
            result = {
                "expected_result": "admin",
                "task_id": index,
                "task": i['task'],
                "role": i['role'],
                "user": i['user'],
                "command": c,
                "malignity_score": jason['malignity_score'],
                "severity_score": jason['severity_score'],
                "utility_score": jason['utility_score'],
                "expectance_score": jason['expectance_score']
            }
            print(json.dumps(result), ",")

        except:
            ...
