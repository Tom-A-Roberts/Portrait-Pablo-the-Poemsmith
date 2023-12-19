import time
import base64
import streamlit as st
import chat_management as chats

st.set_page_config(
    page_title="GPT-4-Vision",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Created by Tom Roberts: https://github.com/Tom-A-Roberts"},
)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "unprocessed_user_message" not in st.session_state:
    st.session_state.unprocessed_user_message = False
if "result" not in st.session_state:
    st.session_state.result = None
if "audio_result" not in st.session_state:
    st.session_state.audio_result = None
def get_api_key():
    if "api_key" not in st.secrets:
        return None
    return st.secrets["api_key"]

api_key = get_api_key()
if api_key == None or api_key == "":
    st.error('No API key set. This needs to be setup in the secrets by the admin.', icon="🚨")
    st.stop()

st.title("Portrait Pablo the Poemsmith 🎙️")
st.caption("A demo of the GPT-4-Vision model, linked with OpenAI's Text-To-Speech AI.")
st.markdown("""
##### How to use
1. You may have to allow access to your camera.
2. Click the camera button to take a photo.
3. Wait for the model to think.

##### How to reset
1. Clear your current photo (press 'Clear Photo')
2. Then click the retry button

##### Additional information
No images are stored, after the model has processed the image it is immediately deleted.

""")
st.divider()

system_prompt = """You are a Caricaturist but you make poems instead of drawings.
Your poems are entertaining and funny and friendly.
They draw upon the image you are shown, creating clever puns about it. Use newlines after each line of the poem.
Don't describe about the background or environment, you are only interested in the people in the image."""
prompt = "Create a medium-sized rhyming poem about the person (or persons) in this image. Maximum of two verses."

camera_container = st.empty()
img_file_buffer = camera_container.camera_input("Take a picture")

if img_file_buffer is not None and st.session_state.result == None:
    # To read image file buffer as bytes:
    system_message = {
        "role": "user",
        "content": [{"type": "text", "text": system_prompt}],
    }
    image = chats.image_file_to_base64(img_file_buffer)
    content = [{"type": "text", "text": prompt}]
    content.append({"type": "image_url", "image_url": {"url": image, "detail": "low"}})
    user_message = {
        "role": "user",
        "content": content,
    }
    chats.add_system_message(system_message, st.session_state.chat_history)
    chats.add_user_message(user_message, st.session_state.chat_history)
    st.session_state.unprocessed_user_message = True
    img_file_buffer.close()
    img_file_buffer = None

def get_text_from_response(message):
    if message == None:
        return ""
    return message.choices[0].message.content

if st.session_state.result != None:
    st.write(get_text_from_response(st.session_state.result))

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

if st.session_state.audio_result != None:
    autoplay_audio(st.session_state.audio_result)

if st.session_state.unprocessed_user_message and st.session_state.result == None:
    with st.spinner("Thinking (Stage 1)"):
        response = chats.get_response(st.session_state.chat_history, api_key)
        st.session_state.result = response
        st.rerun()

if st.session_state.unprocessed_user_message and st.session_state.result != None and st.session_state.audio_result == None:
    with st.spinner("Thinking... (Stage 2)"):
        text_to_speech_file = chats.text_to_speech(get_text_from_response(st.session_state.result), api_key)
        st.session_state.audio_result = text_to_speech_file
        st.session_state.unprocessed_user_message = False
        st.rerun()

if st.session_state.unprocessed_user_message == False and st.session_state.result != None and st.session_state.audio_result != None:
    clear_result = st.button("Retry")
    if clear_result:
        st.session_state.result = None
        st.session_state.audio_result = None
        st.session_state.chat_history = []
        st.session_state.unprocessed_user_message = False
        st.rerun()