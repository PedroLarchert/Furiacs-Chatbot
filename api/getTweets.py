from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json

def get_latest_tweets(username="FURIA", count=3, output_file="./docs/tweets.json"):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=options)
    driver.get(f"https://x.com/{username}")
    time.sleep(5)

    tweets = []
    tweet_elements = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')

    for tweet in tweet_elements[:count]:
        try:
            link_element = tweet.find_element(By.XPATH, './/a[contains(@href, "/status/")]')
            tweet_url = link_element.get_attribute("href")
            if tweet_url:
                tweets.append({"url": tweet_url})
        except:
            continue

    driver.quit()

    # Salva no arquivo JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)

get_latest_tweets()