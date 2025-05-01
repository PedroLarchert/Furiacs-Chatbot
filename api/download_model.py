from huggingface_hub import snapshot_download
import os

model_name = "NousResearch/Hermes-3-Llama-3.1-8B-GGUF"
filename = "Hermes-3-Llama-3.1-8B.Q4_K_M.gguf"
dest_dir = os.path.join(os.path.dirname(__file__), "models")

os.makedirs(dest_dir, exist_ok=True)

print(f"⬇️ Baixando {filename} para {dest_dir}...")

snapshot_download(
    repo_id=model_name,
    allow_patterns=[filename],
    local_dir=dest_dir,
    local_dir_use_symlinks=False
)

print(" Modelo baixado com sucesso!")