import json

with open('dataset_furia_rag_general2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)


for i in data:
    if i["tema"] == "loja":

          i["resposta"] = i["resposta"].replace("link da loja: https://www.furia.gg", "[Acesse o site da FURIA](https://www.furia.gg)")
          


with open('dataset_furia_rag_general2.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

