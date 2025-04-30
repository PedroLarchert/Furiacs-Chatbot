import json
import numpy as np
import faiss
from langchain_community.embeddings import GPT4AllEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

class RAGFuria:
    def __init__(self, caminho_index='./docs/faiss_index_furia.idx'):
        self.embedder = GPT4AllEmbeddings()
        self.caminho_index = caminho_index
        self.index = None
        self.base_completa = None  # Carregamos juntando os dois JSONs

    def carregar_base_e_indexar(self, caminho_agenda, caminho_geral):
        # Carrega dois datasets, gera embeddings e cria o índice FAISS
        with open(caminho_agenda, 'r', encoding='utf-8') as f:
            agenda_data = json.load(f)
        with open(caminho_geral, 'r', encoding='utf-8') as f:
            geral_data = json.load(f)
    
    
        # Juntar bases
        self.base_completa = agenda_data + geral_data

        # Gerar embeddings apenas das perguntas
        perguntas = [item['pergunta'] for item in self.base_completa]
        embeddings = [self.embedder.embed_query(pergunta) for pergunta in perguntas]
        embeddings_array = np.array(embeddings)

        # Criar índice FAISS
        dimension = embeddings_array.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings_array)

        print(f"[RAGFuria] Base carregada e {len(perguntas)} perguntas indexadas.")

    def carregar_base_completa(self, caminho_agenda, caminho_geral):
        """Carrega apenas as perguntas e respostas para trabalhar junto com o FAISS"""
        with open(caminho_agenda, 'r', encoding='utf-8') as f:
            agenda_data = json.load(f)
        with open(caminho_geral, 'r', encoding='utf-8') as f:
            geral_data = json.load(f)

        self.base_completa = agenda_data + geral_data
        print(f"[RAGFuria] Base de perguntas carregada com {len(self.base_completa)} entradas.")

    def salvar_index(self):
        """Salva o índice FAISS em arquivo"""
        if self.index is not None:
            faiss.write_index(self.index, self.caminho_index)
            print("[RAGFuria] Índice FAISS salvo com sucesso!")
        else:
            raise ValueError("Índice FAISS ainda não criado!")

    def carregar_index(self):
        """Carrega o índice FAISS salvo"""
        self.index = faiss.read_index(self.caminho_index)
        print("[RAGFuria] Índice FAISS carregado com sucesso!")

    def buscar_pergunta(self, pergunta_usuario):
        """Busca a melhor resposta para a pergunta do usuário"""
        if self.index is None or self.base_completa is None:
            raise ValueError("Índice ou base completa ainda não carregados.")

        # Gerar embedding da pergunta do usuário
        embedding_usuario = np.array([self.embedder.embed_query(pergunta_usuario)])

        # Buscar similaridade
        D, I = self.index.search(embedding_usuario, k=1)
        idx = I[0][0]

        item = self.base_completa[idx]
        resposta = item['resposta']
        pergunta_associada = item['pergunta']
        tema = item.get('tema', 'Não informado')

        return {
            "pergunta_associada": pergunta_associada,
            "resposta": resposta,
            "tema": tema,
            "similaridade": float(D[0][0])
        }

"""
rag = RAGFuria()
rag.carregar_base_e_indexar('perguntas_respostas_agenda_furia.json', 'dataset_furia_rag_general.json')
rag.salvar_index()
rag.carregar_base_completa(caminho_agenda="perguntas_respostas_agenda_furia.json",caminho_geral="dataset_furia_rag_general.json")
rag.carregar_index()
# Pergunta do usuário
consulta = "quanto foi o jogo da furia contra a red?"

resultado = rag.buscar_pergunta(consulta)

print("Pergunta encontrada:", resultado['pergunta_associada'])
print("Resposta:", resultado['resposta'])
print("Tema:", resultado['tema'])
print("Similaridade:", resultado['similaridade'])
"""