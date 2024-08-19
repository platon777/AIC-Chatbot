import streamlit as st
import openai
from time import sleep
from dotenv import load_dotenv
import os
from helper_functions import create_thread, retrieve_thread, create_message, list_messages, create_run
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Charger les variables d'environnement
load_dotenv()

# Configurer la clé API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configurer la connexion au serveur SQL
server = 'localhost'  
database = 'DataNet' 
username = 'wvalentin'  # Remplacez par votre nom d'utilisateur
password = 'Calibre07*'  # Remplacez par votre mot de passe
driver = 'ODBC Driver 18 for SQL Server'  # Assurez-vous que le driver est installé
connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)

def check_credentials(username, password):
    session = Session()
    try:
        result = session.execute(
            text("SELECT * FROM users WHERE username=:username AND password=:password"),
            {'username': username, 'password': password}
        ).fetchone()
        return result is not None
    finally:
        session.close()

def creds_entered():
    if check_credentials(st.session_state["user"].strip(), st.session_state["passwd"].strip()):
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

def main():
    st.title('Chatbot AIC Assurance vie')

    # Définir votre assistant ID ici
    ASSISTANT_ID = 'asst_auOEyBid2GbfeTD4DQIXAR0X'

    if 'thread_id' not in st.session_state:
        thread = create_thread() 
        st.session_state.thread_id = thread.id

    if 'messages' not in st.session_state:
        st.session_state.messages = list_messages(st.session_state.thread_id)
    else:
        st.session_state.messages = list_messages(st.session_state.thread_id)

    # Afficher les messages
    messages = list(st.session_state.messages) 
    for msg in reversed(messages):
        st.chat_message(msg.role).write(msg.content[0].text.value)

    client = openai.OpenAI()

    with st.sidebar:
        st.header("Directional Prompts")
        if st.button("Comment faire une cotation pour une personne age de 49 ans."):
            st.session_state.user_prompt = "Comment faire une cotation pour une personne age de 49 ans."
        if st.button("C'est quoi l'assurance optima."):
            st.session_state.user_prompt = "C'est quoi l'assurance optima."
        if st.button("Quelles sont les examens a faire pour une assurance vie."):
            st.session_state.user_prompt = "Quelles sont les examens a faire pour une assurance vie."

    prompt_typing = st.chat_input("Enter your message")

    if 'user_prompt' in st.session_state:
        prompt = st.session_state.user_prompt
        del st.session_state.user_prompt
    else:
        prompt = prompt_typing

    if prompt:
        st.chat_message("user").write(prompt)
        create_message(st.session_state.thread_id, "user", prompt)

        with client.beta.threads.runs.create_and_stream(
            thread_id=st.session_state.thread_id,
            assistant_id=ASSISTANT_ID,
            model="gpt-4o",
            instructions=prompt
        ) as stream:
            with st.chat_message("assistant"): 
                response = st.write_stream(stream.text_deltas)
                stream.until_done()

#if authenticate_user():
main()
