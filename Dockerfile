# Utiliza una imagen base
FROM python:3.9

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /src

# Copia los archivos necesarios al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente al contenedor
COPY src /src

# Define el comando de inicio del contenedor
CMD ["python", "taximetro.py"]