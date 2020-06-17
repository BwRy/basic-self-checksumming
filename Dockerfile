FROM python:2.7

RUN apt-get update && apt-get -y upgrade && apt-get -y install git vim python-pip build-essential

WORKDIR /usr/src/app

RUN git clone --depth 1 https://github.com/radareorg/radare2 && cd radare2 && sys/install.sh

RUN git clone --depth 1 https://github.com/mr-ma/basic-self-checksumming


WORKDIR /usr/src/app/basic-self-checksumming

RUN pip install --no-cache-dir -r requirements.txt
RUN python protect.py -p sample.c -f sensitive
RUN python postpatch.py -b out/sample-protected.out -f sensitive -p 222222222 333333333
RUN ./out/sample-protected-patched.out 



