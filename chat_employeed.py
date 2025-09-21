import streamlit as st
from streamlit_chatbox import ChatBox
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

st.title("Chat Employee FAQ")

chat_box = ChatBox(
    use_rich_markdown=True,
    user_theme="green",
    assistant_theme="blue",
)
chat_box.init_session()

chat_box.output_messages()

if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
for var in answer_vars:
    if var not in st.session_state:
        st.session_state[var] = ""

if len(chat_box.history) == 0:
    chat_box.ai_say(questions[0])

if st.session_state.step < len(questions):
    if query := st.chat_input(questions[st.session_state.step]):
        chat_box.user_say(query)
        st.session_state.answers.append(query)
        var_name = answer_vars[st.session_state.step]
        st.session_state[var_name] = query
        st.session_state.step += 1
        # Mostra próxima pergunta, se houver
        if st.session_state.step < len(questions):
            chat_box.ai_say(questions[st.session_state.step])
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
        chat_box.ai_say("Obrigado por compartilhar essas informações!")
        chat_box.ai_say(f"Aqui está o ID da sua empresa gerada: {st.session_state['employee_id']}")
        chat_box.ai_say("Se quiser reiniciar o chat, clique no botão abaixo.")

    if st.button("Reiniciar chat"):
        st.session_state.step = 0
        st.session_state.answers = []
        for var in answer_vars:
            st.session_state[var] = ""
        st.session_state["employee_id"] = None
        chat_box.init_session(clear=True)
        st.rerun()
