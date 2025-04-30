# 🤖 FURIA Chatbot
<img src="assets/Furia.png" alt="FURIA Logo" width="100"/>
Um chatbot inteligente especializado no time de CS2 da FURIA Esports. Responde perguntas sobre jogadores, partidas, estatísticas, loja oficial, e muito mais — utilizando uma LLM local com modelo em formato GGUF.

---

## 🚀 Tecnologias utilizadas

- ⚙️ **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- 🌐 **Frontend**: [Next.js](https://nextjs.org/)
- 🧠 **Modelo LLM**: [Nous Hermes 3 - LLaMA 3.1 8B (GGUF)](https://huggingface.co/NousResearch/Hermes-3-Llama-3.1-8B-GGUF)
- 🧾 **Formato do modelo**: GGUF (usando `llama.cpp`)
- 🔍 **Dados em tempo real**: Scraping da HLTV
- 🐳 **(Opcional)**: Docker para padronização e deploy

---

## 📁 Estrutura do Projeto

```
Furia-Chatbot/
├── api/                         # Backend FastAPI
├── frontend/                    # Frontend Next.js
├── LLM/
│   └── NousResearch/
│       └── Hermes-3-Llama...    # Modelo GGUF
├── scripts/                     # Scripts auxiliares
├── Dockerfile / docker-compose.yml
└── README.md
```

---

## 🛠️ Como rodar o projeto localmente

### 1. Clone o repositório

```bash
git clone https://github.com/PedroLarchert/furia-chatbot.git
cd furia-chatbot
```

### 2. Rodar o backend (FastAPI)

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Rodar o frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

### 4. Rodar o servidor LLM com modelo GGUF

```bash
cd LLM/NousResearch/Hermes-3-Llama-3.1-8B-GGUF
./server.exe -m Hermes-3-Llama-3.1-8B.Q4_K_M.gguf --port 8000 --api
```

> A API da LLM ficará disponível em `http://localhost:8000/v1/chat/completions`

---

## 📌 Funcionalidades

- 🧠 Chatbot treinado com conhecimento sobre a FURIA e CS2
- 📅 Agenda de partidas (via scraping)
- 📊 Resultado de jogadores
- 🛒 Informações sobre a loja oficial
-     Últimos tweets no x (via scraping)

---

## 📦 (Opcional) Rodar com Docker

> Em breve...

---

## 👨‍💻 Autor

Desenvolvido por [Pedro Vitório Larchert de Oliveira](https://github.com/PedroLarchert)  
📫 Entre em contato para colaborações!

---

## 📄 Licença

Este projeto é livre para uso educacional e experimental. Para uso comercial, entre em contato.
