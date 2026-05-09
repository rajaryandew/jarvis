from groq import Groq
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)
def ask_ai(text:str):
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
        {
            "role": "system",
            "content": """
                You are a voice assistant. Give short and consise answers. 
                If the prompt includes tasks like opening a website, ONLY GIVE THE URL in this format `WEB_ACTION actual_url website_name`.
                If the prompt says to create a folder or a directory, return MKDIR folder_name_provided, example: "create a folder named bar inside foo" should return "MKDIR foo/bar", if no nesting is provided, only give the folder name.
                When asked to do air conditioner actions, return `AC_ACTION action_name(turn_on, turn_off, setTemp_n)`
            """
        },
        {
            "role": "user",
            "content": text
        }
        ],
        temperature=1,
        max_completion_tokens=512,
        top_p=1,
        reasoning_effort="low",
        stop=None
    )

    return completion.choices[0].message.content
