# Start this container based on lts of python
FROM python

# we want to work in /code for this container
WORKDIR /code

# copy just the requirements text for running the dependency install
COPY requirements.txt .

# install python requirements
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the rest of the files over to the container (do this after the pip install command for cache optimization)
COPY ./app ./app

# start the api
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5050"]