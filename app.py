import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# =========================================================
# CONFIGURAÇÃO
# =========================================================
load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")

if not api_key:
    raise ValueError("NVIDIA_API_KEY não encontrada. Configure no arquivo .env")

client = OpenAI(
    api_key=api_key,
    base_url="https://integrate.api.nvidia.com/v1",
)

MODEL_NAME = "meta/llama-3.3-70b-instruct"

SYSTEM_PROMPT = """
Você é um assistente especializado em engenharia de prompt.

Seu papel é ajudar o usuário a explorar diferentes estratégias
de construção de prompts para modelos de linguagem.

Sempre que possível:
- explique conceitos de forma objetiva;
- mostre exemplos práticos;
- compare abordagens quando solicitado;
- mantenha respostas técnicas e concisas.
"""

# =========================================================
# STREAMLIT
# =========================================================
st.set_page_config(
    page_title="Engenharia de Prompt",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Engenharia de Prompt")

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.header("Sobre")
    st.markdown("""
Assistente especializado em Engenharia de Prompt.

Faça perguntas sobre:
- Prompt Engineering
- LLMs
- ChatGPT
- Claude
- Gemini
- Agentes
- RAG
- Avaliação de prompts
""")
    st.markdown("---")

    if st.button("Limpar conversa"):
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Olá! Como posso ajudar você com Engenharia de Prompt?"}
        ]
        st.rerun()

# =========================================================
# HISTÓRICO
# =========================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Olá! Como posso ajudar você com Engenharia de Prompt?"}
    ]

# Exibe histórico
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
user_question = st.chat_input("Digite sua pergunta...")

# =========================================================
# PROCESSAMENTO
# =========================================================
if user_question:
    st.session_state.chat_history.append({"role": "user", "content": user_question})

    with st.chat_message("user"):
        st.markdown(user_question)

    # Monta mensagens no formato chat completions
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in st.session_state.chat_history:
        if msg["role"] in ["user", "assistant"]:
            messages.append({"role": msg["role"], "content": msg["content"]})

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    temperature=0.3,
                )
                answer = response.choices[0].message.content
            except Exception as e:
                answer = f"Erro ao consultar o modelo: {e}"

            st.markdown(answer)

    st.session_state.chat_history.append({"role": "assistant", "content": answer})