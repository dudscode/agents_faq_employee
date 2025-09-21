# agentes/agente_employee.py
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from system_prompt.system_prompt import TEXT_EMPLOYEE_AGENT_SYSTEM_PROMPT
import uuid

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.0,
    api_key=api_key
)

def invoke_llm( company_name: str,
                differential: str,
                main_goal: str,
                contact_info: str,
                more_info: str) -> str:
    prompt = TEXT_EMPLOYEE_AGENT_SYSTEM_PROMPT.format(
        company_name=company_name,
        differential=differential,
        main_goal=main_goal,
        contact_info=contact_info,
        more_info=more_info
    )
    response = llm.invoke(prompt)

    unique_id = uuid.uuid4().hex
    pasta_arquivos = "arquivos"
    if not os.path.exists(pasta_arquivos):
        os.makedirs(pasta_arquivos)
    arquivo_saida = f"{pasta_arquivos}/employee_{unique_id}.txt"
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        f.write(response.content)

    return unique_id
