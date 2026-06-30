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
Você é um assistente especializado em hardware e peças de computador.

Seu papel é ajudar o usuário a entender, escolher e comparar componentes de computador,
desde builds simples até setups de alta performance.

Sempre que possível:
- explique os componentes de forma clara e objetiva;
- mostre comparações entre modelos e gerações;
- dê recomendações baseadas em custo-benefício;
- considere compatibilidade entre peças;
- mantenha respostas técnicas mas acessíveis para iniciantes.
"""

# =========================================================
# STREAMLIT
# =========================================================
st.set_page_config(
    page_title="Hardware Advisor",
    page_icon="🖥️",
    layout="wide"
)

st.title("🖥️ Hardware Advisor")

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.header("Sobre")
    st.markdown("""
Assistente especializado em **peças de computador**.

Faça perguntas sobre:
- Processadores (CPU)
- Placas de vídeo (GPU)
- Memória RAM
- Armazenamento (SSD/HDD)
- Placas-mãe
- Fontes de alimentação
- Gabinetes e refrigeração
- Builds completas
- Compatibilidade entre componentes
""")
    st.markdown("---")

    if st.button("Limpar conversa"):
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Olá! Sou seu assistente de hardware. Como posso te ajudar a montar ou melhorar seu computador?"}
        ]
        st.rerun()

# =========================================================
# HISTÓRICO
# =========================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Olá! Sou seu assistente de hardware. Como posso te ajudar a montar ou melhorar seu computador?"}
    ]

# Exibe histórico
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
user_question = st.chat_input("Pergunte sobre peças de computador...")

# =========================================================
# PROCESSAMENTO
# =========================================================
if user_question:
    st.session_state.chat_history.append({"role": "user", "content": user_question})

    with st.chat_message("user"):
        st.markdown(user_question)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in st.session_state.chat_history:
        if msg["role"] in ["user", "assistant"]:
            messages.append({"role": msg["role"], "content": msg["content"]})

    with st.chat_message("assistant"):
        with st.spinner("Analisando componentes..."):
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