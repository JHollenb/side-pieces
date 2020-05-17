FROM staff:_ubuntu18.04

RUN sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list \
    && apt update -y \
    && apt install -y binutils-riscv64-linux-gnu \ 
    && apt build-dep -y qemu-user \
    && cd / \
    && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

ARG PORT
RUN groupmod --gid "$(($PORT + 100000))" ctf
RUN usermod --uid "$(($PORT + 100000))" ctf

COPY init.py /srv/init.py

COPY flag /flag
RUN chmod a-w flag

COPY target /target
COPY run.sh /run.sh
COPY qemu-riscv64 /usr/bin/qemu-riscv64
COPY gdb-riscv64 /usr/bin/gdb-riscv64

ENV TARGET=/run.sh
