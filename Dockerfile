FROM python:3.7-slim

ENV DEBIAN_FRONTEND=noninteractive \
    DEBIAN_FRONTEND=teletype

RUN echo 'deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main' >> /etc/apt/sources.list
RUN apt-get update \
    && apt-get install -y --no-install-recommends apt-utils \
    && apt-get install -y --no-install-recommends git gcc make g++ libgflags-dev libsnappy-dev zlib1g-dev libbz2-dev liblz4-dev libzstd-dev \
    && apt-get autoremove -y && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/rocksdb

RUN git clone https://github.com/facebook/rocksdb.git /tmp/rocksdb \
    && make install-shared INSTALL_PATH=/usr \
    && rm -rf /tmp/rocksdb

ENV STORE_URI=rocksdb://

WORKDIR /faustdemo/

COPY . /faustdemo

RUN if [ -d ".venv" ]; then rm -Rf .venv; fi

RUN pip3 install poetry==1.0.0b1 && poetry add python-rocksdb && poetry install

ENTRYPOINT ["./run.sh"]
