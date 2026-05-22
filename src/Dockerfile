ARG PYTHON_VERSION=3.13

FROM python:${PYTHON_VERSION}-slim

ENV myEnvVar="Local"

WORKDIR /app

COPY main.py .
COPY image.png .

RUN pip install fastapi
RUN pip install uvicorn

EXPOSE 8080

ENTRYPOINT [ "python", "main.py"]
