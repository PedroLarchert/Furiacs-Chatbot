import requests
from rag import RAGFuria


def send_to_llm(mensagem: str,resultado):
    # Endpoint
    url = "http://127.0.0.1:1234/v1/chat/completions"

    # Cabeçalhos (headers)
    headers = {
        "Content-Type": "application/json"
    }

    #rag = RAGFuria()
    #rag.carregar_base_e_indexar('perguntas_respostas_agenda_furia.json', 'dataset_furia_rag_general.json')
    #rag.salvar_index()
    #resultado = rag.buscar_pergunta(mensagem)
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
        response = requests.post(url, headers=headers, json=data, timeout=60 )
        response.raise_for_status()
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

##send_to_llm("quanto foi o jogo da furia contra a astralis?")