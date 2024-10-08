#Creacion dockerfile para la app  de fast

FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos al contenedor
COPY requirements.txt  .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Exponer el puerto de la aplicación
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
