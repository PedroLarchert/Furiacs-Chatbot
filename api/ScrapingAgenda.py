from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json

#A função scraping_agenda() buca no site da hltv as informações das proximas partidas da Furia 

def scraping_agenda():

    # Configurar o Selenium
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    # URL do time da furia na hltv
    url = "https://www.hltv.org/team/8297/furia#tab-matchesBox"
    driver.get(url)

    # Esperar carregar
    time.sleep(5)

    # Pegar HTML carregado
    html = driver.page_source
    driver.quit()

    # Parsear HTML
    soup = BeautifulSoup(html, "html.parser")
    matches_box = soup.find('div', id='matchesBox')

    agenda = []
    current_event = None

    for element in matches_box.find_all(['thead', 'tbody']):
        if element.name == 'thead':
            event_link = element.find('a')
            if event_link:
                current_event = event_link.text.strip()
        elif element.name == 'tbody':
            rows = element.find_all('tr', class_='team-row')
            for row in rows:
                date_cell = row.find('td', class_='date-cell')
                date_text = date_cell.text.strip() if date_cell else "Data desconhecida"

                teams = row.find_all('a', class_='team-name')
                team1 = teams[0].text.strip() if len(teams) > 0 else "Time 1 desconhecido"
                team2 = teams[1].text.strip() if len(teams) > 1 else "Time 2 desconhecido"

                #  Pegar os scores 
                score_spans = row.find('div', class_="score-cell").find_all('span', class_="score")
                score1 = score_spans[0].text.strip() if len(score_spans) > 0 else "-"
                score2 = score_spans[1].text.strip() if len(score_spans) > 1 else "-"

                agenda.append({
                    "evento": current_event,
                    "data": date_text,
                    "time1": team1,
                    "score1": score1,
                    "time2": team2,
                    "score2": score2
                })

    # Salvar como JSON
    output_path = "./docs/agenda_furia.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(agenda, f, ensure_ascii=False, indent=2)

    print(f"Agenda salva em: {output_path}")
