import json
from datetime import datetime


def make_Dataset_Agenda_For_Rag():
    # Carregar o arquivo de agenda
    with open('./docs/agenda_furia.json', 'r', encoding='utf-8') as f:
        agenda = json.load(f)

    # Lista para armazenar os exemplos
    perguntas_respostas = []

    # Data de hoje
    hoje = datetime.now()

    # Separar jogos já jogados e jogos futuros
    jogos_passados = []
    jogos_futuros = []

    for jogo in agenda:
        try:
            # Tentar interpretar como data (ex: 30/04/2025)
            data_jogo = datetime.strptime(jogo['data'], "%d/%m/%Y")
        except ValueError:
            # Se for apenas hora (ex: 03:30), considerar como hoje
            data_jogo = hoje

        if data_jogo.date() < hoje.date():
            jogos_passados.append((data_jogo, jogo))
        else:
            jogos_futuros.append((data_jogo, jogo))

    # Ordenar jogos mais recentes primeiro
    jogos_passados.sort(reverse=True)

    #  Último jogo
    if jogos_passados:
        ultimo_jogo = jogos_passados[0][1]
        data =  datetime.strptime(ultimo_jogo['data'], "%d/%m/%Y")
        pergunta = "Qual foi o último jogo da FURIA?"
        pergunta2= "Quando foi o último jogo da FURIA?"
        resposta = f"O último jogo da FURIA foi contra o time {ultimo_jogo['time2']} Placar: {ultimo_jogo['time1']} {ultimo_jogo['score1']} x {ultimo_jogo['score2']} {ultimo_jogo['time2']} ."
        resposta2 = f"O último jogo da FURIA ocorreu  em {data.strftime('%d/%m/%Y')} contra {ultimo_jogo['time2']} Resultado: {ultimo_jogo['time1']} {ultimo_jogo['score1']} x {ultimo_jogo['score2']} {ultimo_jogo['time2']}."
        perguntas_respostas.append({
            "tema": "agenda",
            "pergunta": pergunta,
            "resposta": resposta
        })
        perguntas_respostas.append({
            "tema": "agenda",
            "pergunta": pergunta2,
            "resposta": resposta2
        })

    #  Últimos jogos
    if jogos_passados:
        pergunta = "Quais foram os últimos jogos da FURIA?"
        resposta_lista = []
        for data, jogo in jogos_passados:
            linha = f"{jogo['time1']} x {jogo['time2']} em {data.strftime('%d/%m/%Y')} (Placar: {jogo['score1']}x{jogo['score2']})"
            resposta_lista.append(linha)
        resposta = "\n".join(resposta_lista)
        perguntas_respostas.append({
            "tema": "agenda",
            "pergunta": pergunta,
            "resposta": resposta
        })

    #  Quanto foi o jogo contra X
    for _, jogo in jogos_passados:
        pergunta = f"Quanto foi o jogo da FURIA contra {jogo['time2']}?"
        resposta = f"O jogo {jogo['time1']} contra {jogo['time2']} no dia {data.strftime('%d/%m/%Y')}, terminou {jogo['time1']} {jogo['score1']}x{jogo['score2']} {jogo['time2']}."
        perguntas_respostas.append({
            "tema": "agenda",
            "pergunta": pergunta,
            "resposta": resposta
        })
        


    #  Próximos adversários
    pergunta = "Quais são os próximos jogos da FURIA?"
    # Verificar se tem jogos futuros
    if not jogos_futuros:

        resposta = "Não há jogos futuros no site da HLTV para a furia, recomendo buscar nas redes sociais oficiais @furiagg ."
        perguntas_respostas.append({
            "tema": "agenda",
            "pergunta": pergunta,
            "resposta": resposta
        })
    else:
        resposta_lista = []
        for data, jogo in jogos_futuros:
            if jogo['data'].count(':') == 1:  # Se for hora (tipo 03:30)
                resposta_lista.append(f"{jogo['time2']} (jogo hoje)")
            else:
                resposta_lista.append(f"{jogo['time2']} no dia {data.strftime('%d/%m/%Y')}")
        
        resposta = "\n".join(resposta_lista)
        perguntas_respostas.append({
            "tema": "agenda",
            "pergunta": pergunta,
            "resposta": resposta
        })


    # Salvar o novo JSON
    with open('./docs/perguntas_respostas_agenda_furia.json', 'w', encoding='utf-8') as f:
        json.dump(perguntas_respostas, f, ensure_ascii=False, indent=2)

    print("Arquivo 'perguntas_respostas_agenda_furia.json' gerado com sucesso!")