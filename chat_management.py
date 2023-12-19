import base64
import time
import openai
from openai import OpenAI, ChatCompletion

global_client = None


def get_client(api_key: str):
    global global_client
    if global_client == None:
        global_client = OpenAI(api_key=api_key)
    return global_client


class SystemMessage:
    def __init__(self, message: dict[str, str or dict]):
        self.role = "system"
        self.message = message

    def to_dict(self):
        return self.message

    def get_text(self):
        return self.message["content"][0]["text"]

class UserMessage:
    def __init__(self, message: dict[str, str or dict]):
        self.role = "user"
        self.message = message

    def to_dict(self):
        return self.message

    def get_text(self):
        return self.message["content"][0]["text"]

    def get_images(self):
        return [content["image_url"]["url"] for content in self.message["content"] if content["type"] == "image_url"]

class AssistantMessage:
    def __init__(self, raw_result: ChatCompletion):
        self.role = "assistant"
        self.raw_result: ChatCompletion = raw_result

    def to_dict(self):
        return {"role": self.role, "content": [{"type": "text", "text": self.raw_result.choices[0].message.content}]}

    def get_text(self):
        return self.raw_result.choices[0].message.content

def image_file_to_base64(image_file):
    image = base64.b64encode(image_file.read()).decode('utf-8')
    image = "data:image/png;base64," + image
    return image

def history_to_dict(history: list[UserMessage or AssistantMessage]):
    return [message.to_dict() for message in history]


def add_system_message(message: dict[str, str or dict], chat_history: list):
    # chat_history.append({"role": "user", "content": [{"type": "text", "text": message}]})
    chat_history.append(SystemMessage(message))

def add_user_message(message: dict[str, str or dict], chat_history: list):
    # chat_history.append({"role": "user", "content": [{"type": "text", "text": message}]})
    chat_history.append(UserMessage(message))

def add_assistant_message(message: ChatCompletion, chat_history: list):
    # chat_history.append({"role": "assistant", "content": [{"type": "text", "text": message}]})
    chat_history.append(AssistantMessage(message))


def get_response(chat_history: list, api_key: str):
    client = get_client(api_key)
    history_dict = history_to_dict(chat_history)
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=history_dict,
        max_tokens=300,
    )
    add_assistant_message(response, chat_history)
    return response

def text_to_speech(text: str, api_key: str):
    client = get_client(api_key)
    speech_file_path = "speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="fable",
        input=text
    )
    response.stream_to_file(speech_file_path)
    return speech_file_path

