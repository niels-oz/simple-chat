import os
from dotenv import load_dotenv
import openai
import streamlit as st
from streamlit_chat import message

# set OpenAI model ID and system message
MODEL = 'gpt-3.5-turbo'
SYSTEM_MESSAGE = {'role': 'system', 'content': 'You are a helpful assistant.'}

# sets env vars as defined in .env
_ = load_dotenv()

# Set OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']

# Setting page title and header
st.set_page_config(page_title='Simple Chat', page_icon=':robot_face:')
st.header('A simple ChatBot')

# Initializing session state variables
if 'messages' not in st.session_state:  # messages contains the complete chat
    st.session_state['messages'] = [SYSTEM_MESSAGE, ]  # initialise chat history with system message
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = 0


# generate a response
def get_completion(prompt):
    st.session_state['messages'].append({'role': 'user', 'content': prompt})  # adding user input to chat history

    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({'role': 'assistant', 'content': response})  # adding response to chat history

    print(completion)
    return response, completion.usage.total_tokens


# container for chat history
response_container = st.container()

# container for text input
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area('You:', key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output, total_tokens = get_completion(prompt=user_input)
        st.session_state['total_tokens'] += total_tokens

    # reset everything
    if st.button('Clear Conversation', key='clear'):
        st.session_state['messages'] = [SYSTEM_MESSAGE, ]
        st.session_state['total_tokens'] = 0

with response_container:
    message('Hello! How can I help you?')
    for i, msg in enumerate(st.session_state['messages']):
        if msg.get('role') == 'user':
            message(msg.get('content'), is_user=True, key=f'{i}_user')
        elif msg.get('role') == 'assistant':
            message(msg.get('content'), key=f'{i}_bot')

st.write(f"total tokens of the current conversation: {st.session_state['total_tokens']}")
