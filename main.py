import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

# Inicializar cliente Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI(title="API IA con Groq", version="1.0.0")

# -----------------
# CORS (ANY ORIGIN)
# -----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],   # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],   # Todos los headers
)

# ---------
# Modelos
# ---------
class AnalisisRequest(BaseModel):
    cliente: str
    mensaje: str

class AnalisisResponse(BaseModel):
    respuesta_ia: str

# ---------
# Endpoint
# ---------
@app.post("/analizar", response_model=AnalisisResponse)
def analizar_mensaje(data: AnalisisRequest):
    try:
        prompt = f"""
Eres un agente de soporte técnico. 
Analiza el mensaje del cliente y responde SOLO en JSON:
{{
  "tipo": "respuesta_automatica | escalar",
  "prioridad": "alta | media | baja",
  "respuesta": "texto para el cliente"
}}

Mensaje del cliente:
{{
  "cliente": "{data.cliente}",
  "mensaje": "{data.mensaje}"
}}
"""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        respuesta = completion.choices[0].message.content

        return {
            "respuesta_ia": respuesta
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
