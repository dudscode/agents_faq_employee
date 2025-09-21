import streamlit as st
from streamlit_chatbox import ChatBox
from agentes.agente_cliente import question_about_employee_RAG

st.title("Chat Client FAQ")

chat_box = ChatBox(
    use_rich_markdown=True,
    user_theme="green",
    assistant_theme="blue",
)
chat_box.init_session()


chat_box.output_messages()


if len(chat_box.history) == 0:
    chat_box.ai_say("O que gostaria de saber sobre a empresa?")


if query := st.chat_input("Digite sua pergunta:"):
    chat_box.user_say(query)
    resposta = question_about_employee_RAG(query)
    chat_box.ai_say(resposta)


if st.button("Reiniciar chat"):
    chat_box.init_session(clear=True)
    st.rerun()
