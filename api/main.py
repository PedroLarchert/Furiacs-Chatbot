from fastapi import FastAPI,HTTPException
import asyncio
from models import ChatRequest, ChatResponse
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from ScrapingAgenda import scraping_agenda
from make_dataset_agenda import make_Dataset_Agenda_For_Rag
from apscheduler.schedulers.background import BackgroundScheduler
from rag import RAGFuria
from sendToLLM import send_to_llm
import json
import re
from datetime import datetime
from getTweets import get_latest_tweets
rag = RAGFuria()

def atualizar_tudo():
    scraping_agenda()
    make_Dataset_Agenda_For_Rag()
    rag.carregar_base_e_indexar('./docs/perguntas_respostas_agenda_furia.json', './docs/dataset_furia_rag_general.json')
    rag.salvar_index()
    get_latest_tweets()
   
def atualizar_tweet():
    get_latest_tweets()

scheduler = BackgroundScheduler()

def agendar_tarefas():
    scheduler.add_job(atualizar_tudo, 'interval', hours=24)
    scheduler.add_job(atualizar_tweet, 'interval', hours=1)
    scheduler.start()

app = FastAPI()
    


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    atualizar_tudo()
    agendar_tarefas()


def extract_tweet_id(url: str) -> str:
    match = re.search(r"status/(\d+)", url)
    return match.group(1) if match else ""

@app.get("/tweets")
def get_saved_tweets():
    try:
        with open("./docs/tweets.json", "r", encoding="utf-8") as f:
            tweet_urls = json.load(f)

        tweets = []
        for tweet in tweet_urls:
            url = tweet.get("url", "")
            tweet_id = extract_tweet_id(url)
            if tweet_id:
                tweets.append({
                    "id": tweet_id,
                    "url": url
                })

        return tweets

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo de tweets não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler tweets: {str(e)}")




@app.get("/matches")
def get_matches():

    with open('./docs/agenda_furia.json', 'r', encoding='utf-8') as f:
        agenda = json.load(f)

    hoje = datetime.now()
    jogos_passados = []
    jogos_futuros = []

    def parse_datetime(jogo):
        try:
            # Caso data completa (ex: 09/04/2025)
            return datetime.strptime(jogo['data'], "%d/%m/%Y")
        except ValueError:
            # Caso seja apenas um horário (ex: 11:00)
            hora = datetime.strptime(jogo['data'], "%H:%M").time()
            return datetime.combine(hoje.date(), hora)

    for jogo in agenda:
        data_jogo = parse_datetime(jogo)

        if jogo['data'].count("/") == 2:
            # É uma data real, então decidimos se é passada ou futura
            if data_jogo < hoje:
                jogos_passados.append(jogo)
            else:
                jogos_futuros.append(jogo)
        else:
            # É horário — sempre jogo futuro
            jogos_futuros.append(jogo)

    jogos_passados.sort(key=parse_datetime, reverse=True)
    jogos_futuros.sort(key=parse_datetime)

    return {
        "passados": jogos_passados,
        "futuros": jogos_futuros
    }

@app.post("/chatresponse", response_model=ChatResponse)
async def chat_response(request: ChatRequest):
    
    # converter para texto
    mensagem_usuario = request.text
    # buscar por similaridade Dados para auxiliar na resposta com rag
    resultado = rag.buscar_pergunta(mensagem_usuario)
    print(resultado)
    # #enviar para a llm
    resposta, status_code = send_to_llm(mensagem_usuario, resultado)
    # Se foi erro, responde uma mensagem padrão ou personalizada
    if status_code != 200:
        respostaLimpa = f"[Erro] {resposta} Por favor tente mais tarde"
    else:
        respostaLimpa = limpar_resposta(resposta)
    return ChatResponse(reply=respostaLimpa)

def limpar_resposta(texto):
    if "<think>" in texto:
        # Remove tudo que vem até o primeiro pulo de linha depois do <think>
        partes = texto.split("</think>")
        if len(partes) > 1:
            return partes[-1].strip()  # Pega só a parte depois do </think>
    return texto.strip()