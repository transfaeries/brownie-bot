FROM python:3.9 as libbuilder
WORKDIR /app
RUN pip install poetry
RUN python3.9 -m venv /app/venv 
COPY ./pyproject.toml ./poetry.lock /app/
RUN VIRTUAL_ENV=/app/venv poetry install 

# FROM ubuntu:hirsute
FROM debian:bookworm-slim
WORKDIR /app
RUN apt-get update
RUN apt-get install -y python3.9 python3-pip
RUN apt-get clean autoclean && apt-get autoremove --yes && rm -rf /var/lib/{apt,dpkg,cache,log}/
COPY --from=libbuilder /app/venv/lib/python3.9/site-packages /app/
COPY ./brownie.py ./utils.py /app/
WORKDIR /app
ENTRYPOINT ["/usr/bin/python3.9", "/app/brownie.py"]
# CMD ["ls","-l" ]
