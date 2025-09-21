from dotenv import load_dotenv
import os
from system_prompt.system_prompt import CLIENT_AGENT_SYSTEM_PROMPT
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS




load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

employee_id = "675f2157bcc74df286eeecf78fbbee0b"  

pasta = Path("arquivos")
docs = []


arquivos_employee = [f for f in pasta.glob("*employee*")]
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.0,
    api_key=api_key
)


if arquivos_employee:
    for arquivo in arquivos_employee:
        print(f"Arquivo encontrado: {arquivo}")
        loader = TextLoader(arquivo)
        docs.extend(loader.load())
        splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
        chunks = splitter.split_documents(docs)
else:
    print("Nenhuma empresa encontrada.")



embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", api_key=api_key)
if chunks:
    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold":0.3, "k": 4}
    )
else:
    print("Nenhum documento carregado, não é possível criar o vetor store.")

prompt_rag = ChatPromptTemplate.from_messages([
    ("system", CLIENT_AGENT_SYSTEM_PROMPT),
    ("human", "Pergunta: {input} ? \n\nContexto:\n{context}")
])
document_chain = create_stuff_documents_chain(llm, prompt_rag)

def question_about_employee_RAG(pergunta: str) :
    docs_relacionados = retriever.invoke(pergunta)

    if not docs_relacionados:
        return {"answer": "Não sei.",
                "citacoes": [],
                "contexto_encontrado": False}

    answer = document_chain.invoke({"input": pergunta,
                                    "context": docs_relacionados})

    txt = (answer or "").strip()

    return txt

print(question_about_employee_RAG("qual o diferencial da empresa?"))