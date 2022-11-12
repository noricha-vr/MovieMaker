# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.8-buster

# fonts-takao-*                             # jp (Japanese) fonts
# ttf-wqy-microhei fonts-wqy-microhei       # kr (Korean) fonts
# fonts-arphic-ukai fonts-arphic-uming      # cn (Chinese) fonts

# Install manually all the missing libraries
RUN apt-get update && apt-get install -y  \
    ffmpeg\
    gconf-service  \
    libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0  \
    libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget \
    fonts-takao-* ttf-wqy-microhei fonts-wqy-microhei \
    fonts-arphic-ukai fonts-arphic-uming

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# Install Python dependencies.
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .