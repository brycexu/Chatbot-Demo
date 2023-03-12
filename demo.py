import streamlit as st
from streamlit_chat import message
from qa_system import QA

qa = QA()

def generate_response(question):
    # print(question)
    # Run our system here to generate an answer = system.generate_answer(question)
    # answer = "This is a default answer."
    response = qa.answer(question)
    return response

st.title("BNY Mellon Chatbot Project")

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hello there! How may I assist you today?"]

if 'past' not in st.session_state:
    st.session_state['past'] = ["Hello!"]

if 'submit' not in st.session_state:
    st.session_state.submit = ''

if 'widget' not in st.session_state:
    st.session_state.widget = ''

def submit():
    st.session_state.submit = st.session_state.widget
    st.session_state.widget = ''
    user_input = st.session_state.submit
    output = generate_response(user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

input_text = st.text_input("Ask a question: ","", key="widget", on_change=submit)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i), is_user=False)
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
