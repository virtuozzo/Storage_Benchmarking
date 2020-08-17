#!/bin/sh
git clone https://github.com/axboe/fio
sudo apt install -y libc6-dev libaio-dev build-essential git zlib1g-dev python3-pip
wget http://mirror.centos.org/centos/7/os/x86_64/Packages/libaio-0.3.109-13.el7.x86_64.rpm
pip3 install numpy
cd fio
make clean; ./configure --build-static; make
