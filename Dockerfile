FROM debian:stable-slim

RUN apt update
RUN apt install curl git python3-venv pip jq -y
RUN pip3 install streamlit --break-system-packages
