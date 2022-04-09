FROM debian:bookworm-slim
WORKDIR /app
RUN apt-get update
RUN apt-get install -y python3.9 python3-pip
RUN python3.9 -m pip install discord
RUN apt-get clean autoclean && apt-get autoremove --yes && rm -rf /var/lib/{apt,dpkg,cache,log}/
COPY brownie.py /app/
ENTRYPOINT [ "/usr/bin/python3.9", "/app/brownie.py"]
