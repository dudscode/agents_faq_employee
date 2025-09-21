import streamlit as st
from streamlit_chat import message
from agentes.agente_employee import invoke_llm

questions = [
    "Qual o nome da sua empresa?",
    "Agora me conte sobre o principal objetivo da empresa.",
    "Agora me conte o diferencial de vocês.",
    "Me passe uma forma de entrar em contato.",
    "Me conte mais."
]

answer_vars = [
    "company_name",
    "main_goal",
    "differential",
    "contact_info",
    "more_info"
]


if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
for var in answer_vars:
    if var not in st.session_state:
        st.session_state[var] = ""


def next_question(user_input):
    print(f"User input: {user_input}")
    if user_input:
        st.session_state.answers.append(user_input)
        var_name = answer_vars[st.session_state.step]
        st.session_state[var_name] = user_input
        st.session_state.step += 1


def restart_chat():
    st.session_state.step = 0
    st.session_state.answers = []
    for var in answer_vars:
        st.session_state[var] = ""
    st.session_state["employee_id"] = None


chat_container = st.container()

with chat_container:

    for i, ans in enumerate(st.session_state.answers):
        message(questions[i], is_user=False, key=f"bot_{i}")
        message(ans, is_user=True, key=f"user_{i}")


    if st.session_state.step < len(questions):
        current_question = questions[st.session_state.step]
        message(current_question, is_user=False, key=f"bot_current_{st.session_state.step}")


        col1, col2 = st.columns([4,1])

        with col1:
            if st.session_state.step == len(questions) - 1:
                user_input = st.text_area("Sua resposta:", key=f"input_{st.session_state.step}", height=100)
            else:
                user_input = st.text_input("Sua resposta:", key=f"input_{st.session_state.step}")

        with col2:
            st.write("") 
            st.write("")
            if st.button("Enviar", key=f"button_{st.session_state.step}"):
                next_question(st.session_state[f"input_{st.session_state.step}"])
                st.rerun()

    else:
        if "employee_id" not in st.session_state or st.session_state["employee_id"] is None:
            loader_placeholder = st.empty()
            loader_placeholder.info("Processando suas respostas... ⏳")
            st.session_state["employee_id"] = invoke_llm(
                st.session_state.company_name,
                st.session_state.differential,
                st.session_state.main_goal,
                st.session_state.contact_info,
                st.session_state.more_info
            )
            loader_placeholder.empty()
        message("Obrigado por compartilhar essas informações!", is_user=False, key="final_bot")
        st.write("Aqui está ID da sua empresa gerada:")
        st.write(st.session_state["employee_id"])
        st.write("Se quiser reiniciar o chat, clique no botão abaixo:")
        if st.button("Reiniciar chat"):
            restart_chat()
            chat_container.empty()
            st.rerun()
