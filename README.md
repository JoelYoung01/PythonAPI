# Python API

## Setting up for Development

Here is a quick guide to setting up your development environment for the Python API.

### Prerequisites

* [Python 3.9+](https://www.python.org/downloads/release/python-370/)
* [Docker](https://www.docker.com/)
* [Visual Studio Code](https://code.visualstudio.com/) (recommended IDE)

### Setup

1. Add setup steps here

## Running the API locally

Have the Local Db Container running. Then, run the following command to start the API:

```bash
uvicorn app.main:app --reload
```

Alternatively, you can run the api in a container by running the following command:

```bash
docker run --rm -it -p 5050:5050/tcp --env-file .env --name pythonapi <image_name>
```

Don't forget to replace `<image_name>` with the name of the image you built, for example `joelyoung01/pythonapi:latest`.
