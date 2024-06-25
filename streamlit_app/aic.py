import streamlit as st
import openai
from time import sleep
from dotenv import load_dotenv
import os
from helper_functions import create_thread, retrieve_thread, create_message, list_messages, create_run
from openai import OpenAI
import pyodbc
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")



def creds_entered():
    if st.session_state["user"].strip() == "admin" and st.session_state["passwd"].strip() == "admin":
        st.session_state["authenticated"] = True
    else:
        st.session_state["authenticated"] = False
        st.error("Invalid Username/Password :face_with_raised_eyebrow:")

def authenticate_user():
    if "authenticated" not in st.session_state:
        st.text_input(label="Username", value="", key="user", on_change=creds_entered)
        st.text_input(label="Password", value="", key="passwd", type="password", on_change=creds_entered)
        return False
    
    else: 
        if st.session_state["authenticated"]:
            return True
        else:
            st.text_input(label="Username", value="", key="user", on_change=creds_entered)
            st.text_input(label="Password", value="", key="passwd", type="password", on_change=creds_entered)
            return False
    


if authenticate_user():
    
    st.title('Chatbot AIC Assurance vie')

    # Set your assistant ID here
    ASSISTANT_ID = 'asst_auOEyBid2GbfeTD4DQIXAR0X'

    if 'thread_id' not in st.session_state:
        thread = create_thread() 
        st.session_state.thread_id = thread.id

    if 'messages' not in st.session_state:
        st.session_state.messages = list_messages(st.session_state.thread_id)
    else:
        st.session_state.messages = list_messages(st.session_state.thread_id)


    

    # Display messages
    messages  = list(st.session_state.messages) 
    for msg in reversed(messages):
        st.chat_message(msg.role).write(msg.content[0].text.value)


    #prompt = st.chat_input("Enter your message")

    client = openai.OpenAI()

    with st.sidebar:
        st.header("Directional Prompts")
        if st.button("Comment faire une cotation pour une personne age de 49 ans."):
            st.session_state.user_prompt =  "Comment faire une cotation pour une personne age de 49 ans."
        if st.button("C'est quoi l'assurance optima."):
            st.session_state.user_prompt = "C'est quoi l'assurance optima."
        if st.button("Quelles sont les examens a faire pour une assurance vie."):
            st.session_state.user_prompt = "Quelles sont les examens a faire pour une assurance vie."

    if 'user_prompt' in st.session_state:
        prompt = st.session_state.user_prompt
        del st.session_state.user_prompt
    else:
        prompt = st.chat_input("Enter your message")


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


    

