from pydantic import BaseModel

# Modelo para entrada
class ChatRequest(BaseModel):
    text: str

# Modelo para saída (opcional, mas recomendado)
class ChatResponse(BaseModel):
    reply: str
