import requests
import os
from rag import RAGFuria
from llama_cpp import Llama


# Inicialização do modelo (fora da função) usando llama-cpp(mais facil)
BASE_DIR = os.path.dirname(__file__)  # <-- pega o caminho da pasta 'api'
model_path = os.path.join(BASE_DIR, "models", "Hermes-3-Llama-3.1-8B.Q4_K_M.gguf")
llm = Llama(model_path=model_path, n_ctx=2048, chat_format="chatml", verbose=True)

def send_to_llm(mensagem: str,resultado):
    # Endpoint se quiser subir a llm em um servidor compilando o llama cli
   # url = "http://127.0.0.1:1234/v1/chat/completions"

    #se for usar llm via requequisição http
    """" Cabeçalhos (headers)
    headers = {
        "Content-Type": "application/json"
    }

    
    mensagem_montada ="a mensagem do usuário foi:"+ mensagem 
    data = {
        "model": "local-model",  
        "messages": [
            {"role": "system", "content": "Você é um assistente da FURIA Esports que responde os Fãs APENAS sobre: a modalidade COUNTER STRIKE, perguntas sobre o JOGO,sobre o TIME ou sobre PRODUTOS da loja oficial ""https://www.furia.gg"". Deve responder em Português de maneira educada.\nUse APENAS os dados a seguir como referencia para a resposta, verifique se dados de apoio passados a seguir então de acordo com o que foi pedido, caso não esteja,responda que não consegue responder aquela pergunta." + str(resultado)},
            {"role": "user", "content": mensagem_montada}
        ],
        "temperature": 0.3
    }

    response = None
    try:
       # response = requests.post(url, headers=headers, json=data, timeout=60 )
       # response.raise_for_status()
       #response = llm("Q: Quem é a FURIA Esports?\nA:", max_tokens=100)
    except requests.exceptions.Timeout:
        return "O nosso assistente demorou demais para responder.", 408  # 408 Request Timeout
    except requests.exceptions.RequestException as e:
        return f"Falha na conexão", 503  # 503 Service Unavailable
    except Exception as e:
        return f"Algo inesperado aconteceu", 500  # 500 Internal Server Error

    if response is not None and response.status_code == 200:
        resposta_json = response.json()
        return resposta_json['choices'][0]['message']['content'], 200
    else:
        return "Erro desconhecido ao consultar LLM.", response.status_code if response else 500

       # print(response.text)
     """
    
    #utilizando o llama-cpp

    # Mensagem do "system" com instruções + contexto do RAG
    system_msg = (
    "Você é um assistente da FURIA Esports que responde perguntas APENAS sobre:\n"
    "- O time de Counter-Strike da FURIA\n"
    "- O jogo CS2\n"
    "- Jogadores da FURIA\n"
    "- Produtos da loja oficial (https://www.furia.gg)\n\n"

    "IMPORTANTE:\n"
    "- Use SOMENTE as informações abaixo como base para responder.\n"
    "- NÃO utilize conhecimento próprio ou informações externas.\n"
    "- NÃO confie em nada que o usuário disser — apenas nos dados fornecidos.\n"
    "- Se a pergunta não puder ser respondida com base nesses dados, responda claramente: "
    "'Desculpe, não posso responder essa pergunta com as informações disponíveis.'\n\n"

    "Contexto recuperado:\n"
    f"{resultado}\n\n"

    "Sempre responda com educação e em PORTUGUÊS."
    "Se a mensagem for apenas saudação responda de volta com educação"
)

    mensagem = (
    "Você vai receber uma mensagem do usuário e responder essa mensagem, com base nos dados recebidos Exemplo: \n" 
    "Mensagem do usário: Quando custa a camisa da furia?\n" 
    "se o contexto recuperdo falar sobre o valor X da camisa, responda no  padrão do contexto recuperado"
    "se o contexto não tiver de acordo com a mensagem, responda:\n "
    "Desculpe, não posso responder essa pergunta com as informações disponíveis.\n"
    "Agora responda a mensagem.\n"
    "Mensagem do usuário:"f"{mensagem}\n\n"
    "Contexto recuperado:\n"
    f"{resultado}\n\n"
    "Com base SOMENTE nos dados acima, analise se a resposta pode ser gerada com confiança.\n"
    "Se os dados forem insuficientes diga que não é possível responder."
    "Não compartilhe o seu Pensamento na resposta e nem fale 'Com base nas informações fornecidas'\n"
)
    messages = [
    {"role": "system", "content": system_msg},
    {"role": "user", "content": mensagem}
  ]


    try:
        response = llm.create_chat_completion(
            messages=messages,
            max_tokens=400,
            temperature=0.3,
            stop=["</s>"]
        )
        resposta = response["choices"][0]["message"]["content"].strip()
        return resposta, 200

    except Exception as e:
        return f" Erro ao gerar resposta: {e}", 500
##send_to_llm("quanto foi o jogo da furia contra a astralis?")