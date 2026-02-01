FROM python:3-slim

# Directorio de trabajo
WORKDIR /api-agente

# Instalar dependencias Python
RUN pip install fastapi uvicorn groq python-dotenv

# Copiar aplicación
COPY . .

# Comando de ejecución
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]