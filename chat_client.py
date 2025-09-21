import streamlit as st
from streamlit_chat import message
from agentes.agente_cliente import question_about_employee_RAG
import time

questions = [
    "O que gostaria de saber sobre a empresa?",
]

answer_vars = [
    "user_question",
]



if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "ask_more" not in st.session_state:
    st.session_state.ask_more = False
for var in answer_vars:
    if var not in st.session_state:
        st.session_state[var] = ""
if "answer" not in st.session_state:
    st.session_state["answer"] = None
if "history" not in st.session_state:
    st.session_state.history = []
if "questions" not in st.session_state:
    st.session_state.questions = questions.copy()


def next_question(user_input):
    if user_input:
        st.session_state.answers.append(user_input)
        if st.session_state.step < len(answer_vars):
            var_name = answer_vars[st.session_state.step]
            st.session_state[var_name] = user_input
        st.session_state.step += 1
        st.session_state["answer"] = None  

def restart_chat():
    st.session_state.step = 0
    st.session_state.answers = []
    st.session_state.ask_more = False
    st.session_state["answer"] = None
    st.session_state.history = []
    for var in answer_vars:
        st.session_state[var] = ""

chat_container = st.container()

with chat_container:
    for i, ans in enumerate(st.session_state.answers):
        if(i == 0):
            message(questions[0], is_user=False, key=f"bot_{i}")
        else:
            message(st.session_state.questions[-1], is_user=False, key=f"one_{i}")
            message("Posso te ajudar com mais alguma coisa?", is_user=False, key=f"two{i}")

        message(ans, is_user=True, key=f"user_{i}")

    
    if st.session_state.step < len(questions):
        current_question = questions[st.session_state.step]
        message(current_question, is_user=False, key=f"bot_current_{st.session_state.step}")

        col1, col2 = st.columns([4,1])
        with col1:
            user_input = st.text_input("Sua pergunta:", key=f"input_{st.session_state.step}")
        with col2:
            st.write("") 
            st.write("")
            if st.button("Enviar", key=f"button_{st.session_state.step}"):
                next_question(st.session_state[f"input_{st.session_state.step}"])
                st.rerun()


    
    else:
        
        if st.session_state["answer"] is None:
            loader_placeholder = st.empty()
            loader_placeholder.info("Processando a pergunta... ⏳")
           
            last_question = st.session_state.answers[-1]
            st.session_state["answer"] = question_about_employee_RAG(last_question)
            loader_placeholder.empty()
            st.session_state.history.append(st.session_state["answer"])
            st.session_state.questions.append(st.session_state["answer"])
        message(st.session_state["answer"], is_user=False, key=f"final_bot_{len(st.session_state.answers)}")

        
        if not st.session_state.ask_more:
            message("Posso te ajudar com mais alguma coisa?", is_user=False, key=f"ask_more_{len(st.session_state.answers)}")
            col1, col2 = st.columns([4,1])
            with col1:
                more_input = st.text_input("Digite sua pergunta:", key=f"more_input_{len(st.session_state.answers)}")
            with col2:
                st.write("")
                st.write("")
                if st.button("Enviar", key=f"button_more_{len(st.session_state.answers)}"):
                    if more_input.strip().lower() in ["não", "nao", "n"]:
                        st.session_state.ask_more = True
                    elif more_input.strip() != "":
                        st.session_state.answers.append(more_input)
                        st.session_state["answer"] = None  
                        st.rerun()

        if st.session_state.ask_more:
            st.write("Obrigado por usar o chat!")
            if st.button("Reiniciar chat"):
                restart_chat()
                chat_container.empty()
                st.rerun()
