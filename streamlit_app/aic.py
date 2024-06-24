import streamlit as st
import openai
from time import sleep
from dotenv import load_dotenv
import os
from helper_functions import create_thread, retrieve_thread, create_message, list_messages, create_run
from openai import OpenAI


load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set your assistant ID here
ASSISTANT_ID = 'asst_auOEyBid2GbfeTD4DQIXAR0X'

if 'thread_id' not in st.session_state:
    thread = create_thread() 
    st.session_state.thread_id = thread.id

if 'messages' not in st.session_state:
    st.session_state.messages = list_messages(st.session_state.thread_id)
else:
     st.session_state.messages = list_messages(st.session_state.thread_id)


st.title('Chatbot AIC Assurance vie')

# Display messages
messages  = list(st.session_state.messages) 
for msg in reversed(messages):
    st.chat_message(msg.role).write(msg.content[0].text.value)


prompt = st.chat_input("Enter your message")

client = openai.OpenAI()
if prompt:

    #st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    create_message(st.session_state.thread_id, "user", prompt)



    with client.beta.threads.runs.create_and_stream(

        thread_id = st.session_state.thread_id,
        assistant_id = ASSISTANT_ID,
        model = "gpt-4o",
        instructions=prompt
    ) as stream:
        with st.chat_message("assistant"): 
            response = st.write_stream(stream.text_deltas)
            stream.until_done()

    

