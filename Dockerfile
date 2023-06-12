# Utiliza una imagen base
FROM python:3.9

# Establece el directorio de trabajo dentro del contenedor
# WORKDIR /app

# Copia los archivos necesarios al contenedor
# COPY requirements.txt .

# Instala las dependencias
# RUN pip install -r requirements.txt

# Copia el código fuente al contenedor
COPY . .

# Define el comando de inicio del contenedor
# CMD ["python", "main.py"]
