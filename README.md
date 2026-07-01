# 🖥️ Hardware Advisor — Chatbot com LLaMA 3.3 + NVIDIA + Oracle Cloud

> Relatório técnico — Disciplina de Produtos de GenAI

---

## Introdução

### Objetivo da atividade

Esta atividade teve como objetivo desenvolver e implantar um chatbot baseado em Inteligência Artificial Generativa utilizando um modelo open source disponibilizado pela NVIDIA. A aplicação foi desenvolvida em Python com Streamlit e publicada em uma máquina virtual na Oracle Cloud Infrastructure (OCI), tornando-a acessível publicamente via navegador web.

### Visão geral da solução desenvolvida

A solução consiste em um chatbot especializado em **hardware e peças de computador**, capaz de responder perguntas sobre processadores, placas de vídeo, memória RAM, armazenamento, compatibilidade entre componentes e montagem de builds completas. A interface foi construída com Streamlit, mantendo histórico de conversa na sessão, e o backend consome a API da NVIDIA via protocolo compatível com OpenAI.

---

## Infraestrutura

### Configuração da máquina virtual

| Recurso | Configuração |
|---|---|
| Provedor | Oracle Cloud Infrastructure (OCI) |
| Shape | VM.Standard.E2.1.Micro |
| OCPU | 1 |
| Memória | 1 GB |
| Rede | 0.48 Gbps |
| Disco | Block Storage |
| Região | Brazil East (São Paulo) |
| IP público | Ephemeral IPv4 |

### Sistema operacional utilizado

Ubuntu Server 22.04 LTS (Canonical)

### Recursos computacionais disponíveis

A instância utilizada é elegível ao nível **Always Free** da Oracle Cloud, com 1 OCPU e 1 GB de RAM — suficiente para hospedar a aplicação Streamlit com consumo de API remota, sem necessidade de GPU local.

---

## Modelo Escolhido

### Nome do modelo

`meta/llama-3.3-70b-instruct`

### Justificativa da escolha

O LLaMA 3.3 70B Instruct foi escolhido por ser um dos modelos open source mais capazes disponíveis na plataforma NVIDIA NIM. Com 70 bilhões de parâmetros e fine-tuning para seguir instruções, ele oferece respostas técnicas de alta qualidade — ideal para um assistente especializado em hardware, onde precisão e profundidade técnica são essenciais.

### Principais características

- 70 bilhões de parâmetros
- Otimizado para seguir instruções (instruct)
- Suporte a contexto longo
- Disponível via API compatível com OpenAI (NVIDIA NIM)
- Multilíngue, com excelente desempenho em português

---

## Desenvolvimento

### Arquitetura da aplicação

```
Usuário (navegador)
      ↓
Streamlit (app.py) — porta 8501
      ↓
OpenAI SDK (base_url: integrate.api.nvidia.com)
      ↓
NVIDIA NIM API → meta/llama-3.3-70b-instruct
```

- Interface: Streamlit com histórico de mensagens via `st.session_state`
- Backend: cliente OpenAI apontando para a API da NVIDIA
- System prompt especializado em hardware e peças de computador

### Bibliotecas utilizadas

| Biblioteca | Versão | Finalidade |
|---|---|---|
| streamlit | 1.40.1 | Interface web |
| openai | 1.57.2 | Consumo da API NVIDIA NIM |
| python-dotenv | 1.0.1 | Gerenciamento de variáveis de ambiente |

### Estratégia de gerenciamento de credenciais

A chave de API da NVIDIA (`NVIDIA_API_KEY`) é armazenada em um arquivo `.env` local na máquina virtual, que **não é versionado** (incluído no `.gitignore`). A aplicação carrega a variável em tempo de execução via `python-dotenv`, mantendo as credenciais fora do repositório.

---

## Implantação

### Processo de publicação na Oracle Cloud

1. Criação da instância VM.Standard.E2.1.Micro na OCI (região São Paulo)
2. Configuração da VCN com subnet pública e Internet Gateway
3. Acesso via SSH com chave privada
4. Instalação do Python 3, criação de ambiente virtual (`.venv`)
5. Clone do repositório e instalação das dependências via `pip install -r requirements.txt`
6. Configuração do arquivo `.env` com a `NVIDIA_API_KEY`
7. Execução da aplicação com `nohup streamlit run app.py --server.address 0.0.0.0 --server.port 8501`

### Principais desafios encontrados

- **Security List da OCI**: necessário adicionar regra de Ingress TCP para a porta 8501 manualmente.
- **iptables do Ubuntu**: a imagem padrão da OCI bloqueia portas por firewall local (`iptables`), mesmo com Security List liberada. A solução foi adicionar a regra manualmente:
  ```bash
  sudo iptables -I INPUT -p tcp --dport 8501 -j ACCEPT
  sudo apt install iptables-persistent -y
  sudo netfilter-persistent save
  ```
- **IP Ephemeral**: o IP público é efêmero, podendo mudar após reboot da instância.

---

## Discussão

### Lições aprendidas

- A OCI possui duas camadas de firewall independentes: **Security List** (nível de rede) e **iptables** (nível do sistema operacional). Ambas precisam estar configuradas para que a aplicação seja acessível externamente.
- Modelos de 70B via API remota eliminam a necessidade de GPU local, tornando a implantação viável em instâncias Always Free.
- O Streamlit é uma ferramenta poderosa para prototipagem rápida de interfaces de IA, com curva de aprendizado baixa.

### Possíveis melhorias futuras

- Substituir IP Ephemeral por IP Reserved para estabilidade da URL
- Adicionar autenticação básica na interface
- Permitir troca de modelo via sidebar
- Adicionar streaming de respostas para melhor UX
- Containerizar a aplicação com Docker para facilitar reprodutibilidade
- Expandir o escopo para recomendações de builds com base em orçamento

---

## Instalação e Execução

### Pré-requisitos

- Python 3.10+
- Conta na [NVIDIA NIM](https://build.nvidia.com/) com API Key

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/GuilhermeGirata/chatbot_genai.git
cd chatbot_genai

# 2. Crie o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure a chave de API
echo "NVIDIA_API_KEY=sua_chave_aqui" > .env

# 5. Execute a aplicação
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### Acesso

Abra no navegador: `http://localhost:8501`  
Em produção (OCI): `http://163.176.224.35:8501`

---

## Autor

**Guilherme Cicarello Girata**  
Disciplina de Produtos de GenAI  
2026