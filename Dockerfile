FROM  python:3.8.13-bullseye

ENV PYTHONUNBUFFERED=1

WORKDIR /server



# copy from the current directory of the Dockerfile to /api in the image
COPY . . 

RUN pip install -r requirements.txt

EXPOSE 8000