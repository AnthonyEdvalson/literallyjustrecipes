from typing import List
import openai
import os

openai.organization = os.getenv("OPEN_AI_ORG")
openai.api_key = os.getenv("OPEN_AI_KEY")


def chat(messages: List[str], temperature: float):
    streamed_response = stream_chat(messages, temperature)

    response = ""
    line_len = 0
    print("<<< ", end="")
    for chunk in streamed_response:
        response += chunk

        nl = False
        for char in chunk:
            if char == "\n" and nl:
                line_len = 0
                print("\n<<<\n<<<", end="")
            elif char == "\n" and not nl:
                nl = True
            elif char == " " and line_len > 70:
                nl = False
                line_len = 0
                print("\n<<< ", end="")
            else:
                nl = False
                line_len += 1
                print(char, end="")

    return response


def stream_chat(messages: List[str], temperature: float):
    msgs = []
    role = "user"
    for msg in messages:
        msgs.append({
            "role": role,
            "content": msg
        })
        role = "user" if role == "system" else "system"

    print("===")
    for msg in msgs:
        tag = "usr" if msg["role"] == "user" else "sys"
        print(">>> ({}) {}".format(tag, msg["content"]))
    streamed_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msgs,
        temperature=temperature,
        max_tokens=1536,
        stream=True,
        stop=["INGREDIENTS:", "Ingredients:"]
    )

    for chunk in streamed_response:
        choice = chunk.choices[0]
        if choice.finish_reason is not None:
            break
        delta = choice.delta
        if "content" in delta:
            yield delta.content
