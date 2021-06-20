FROM python:3.7-slim-stretch
LABEL maintainer="<s.ritwik98@gmail.com>"
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND noninteractive
ENV BUILD_VERSION '0.1.1'
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code_service
RUN apt-get -yq update && \
    apt-get -yq upgrade && \
    apt-get -yq --no-install-recommends install \
	g++ \
	dnsutils \
	wget \
	libc6-dev \
	libssl-dev \
	apt-transport-https \
	ca-certificates \
	libcurl4-openssl-dev \
	libgnutls28-dev \
	vim && \
    apt-get clean && \
    rm -rf /tmp/* /var/tmp/* /var/lib/apt/archive/* /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install -U pip
# RUN apt-get purge -y --auto-remove g++
RUN pip install -r requirements.txt
ADD ./ /code_service
