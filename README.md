<!-- ABOUT THE PROJECT -->
## About The Project

This repository is a backend part of Customer Conversational Intelligence Platform Powered by an LLM Agent. This is created with help of [![fastapi][fast-image]][fast-url] [![Ollama][ollama-image]][ollama-url] [![Phi3][phi3-image]][phi3-url]

<!-- GETTING STARTED -->
## Getting Started

You can run this locally as either as a python app or as a docker container.

## Running without docker

### Create virtual Environment
```
Follow below steps:

$ git clone https://github.com/Group3AIMLops/ollama_chatbot_backend.git
$ cd ollama_chatbot_backend
$ python -m venv venv     or  python -m venv <Project_Path>\venv
```

### Activate Python virtual Environment
```
$ ./venv/Scripts/activate 
```

### Create .env file

```
create .env file with below data

use_sql = False (False if you dont want to connect to database)
```

### Install dependencies

```
$ pip install -r requirements.txt
```

### Run the application

```
You can run app with below command

$ python api/app.py
```

## Running with docker

Make sure you have installed docker

### Pull docker image

```
$ docker image pull sumanthegdedocker/chatbot_backend:latest
```

### Run docker image

if you want to run on GPU

```
$ docker run --rm --runtime=nvidia --gpus all -d -e use_sql="False" -p 8001:8001 sumanthegdedocker/chatbot_backend:latest
```

If you dont have GPU

```
$ docker run -d -e use_sql="False" -p 8001:8001 sumanthegdedocker/chatbot_backend:latest
```

## Other related repos

you can checkout backend part of this project here 

[frontend repo][frontend-url], [operations repo][operations-url]



<!-- MARKDOWN LINKS & IMAGES -->
[fast-image]: https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png
[fast-url]: https://fastapi.tiangolo.com/
[ollama-image]: https://ollama.com/public/ollama.png
[ollama-url]: https://ollama.com/
[phi3-image]: https://img-prod-cms-rt-microsoft-com.akamaized.net/cms/api/am/imageFileData/RE1Mu3b?ver=5c31
[phi3-url]: https://ollama.com/library/phi3
[frontend-url]: https://github.com/Group3AIMLops/ollama_chatbot_frontend
[operations-url]: https://github.com/Group3AIMLops/gp3_capstone_iac
