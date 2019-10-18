FROM python:3.7-slim

ENV DEBIAN_FRONTEND=noninteractive \
    DEBIAN_FRONTEND=teletype

RUN echo 'deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main' >> /etc/apt/sources.list
RUN apt-get update \
    && apt-get install -y --no-install-recommends apt-utils \
    && apt-get install -y --no-install-recommends git gcc make g++ libgflags-dev libsnappy-dev zlib1g-dev libbz2-dev liblz4-dev libzstd-dev netcat\
    && apt-get autoremove -y && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/rocksdb

RUN git clone https://github.com/facebook/rocksdb.git /tmp/rocksdb \
    && make install-shared INSTALL_PATH=/usr \
    && rm -rf /tmp/rocksdb

ENV STORE_URI=rocksdb://

WORKDIR /faustdemo/

COPY run.sh /faustdemo/
COPY wait_for_services.sh /faustdemo/
COPY poetry.lock /faustdemo/
COPY poetry.toml /faustdemo/
COPY pyproject.toml /faustdemo/
COPY Makefile /faustdemo/

RUN pip3 install poetry==1.0.0b1 && poetry add python-rocksdb && poetry install

COPY faustdemo /faustdemo/faustdemo

ENTRYPOINT ["./run.sh"]
