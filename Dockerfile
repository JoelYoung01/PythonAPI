# Build from python 3.10 slim
FROM python:3.11

# we want to work in /code for this container
WORKDIR /app

# copy just the requirements text for running the dependency install
COPY requirements.txt .

# install python requirements
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the files over to the container (do this after the pip install command for cache optimization)
COPY app .

WORKDIR /

EXPOSE 5050

# start the api
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5050"]