#!/bin/sh
echo "XXX start"
echo "$1"
dev=$1
dd if=/dev/urandom of=$dev bs=4M count=1000 conv=sync
fio --name randread --direct=1 --filename=$dev --rw=randread --size=2g  --bs=4k --ioengine=libaio --fsync=1 --iodepth=8 --numjobs=32 --runtime=60 --group_reporting
echo "XXX randread"
fio --filename=$dev --direct=1 --rw=randrw --refill_buffers --norandommap --randrepeat=0 --ioengine=libaio --bs=4k --rwmixread=100 --iodepth=16 --numjobs=16 --runtime=60 --group_reporting --name=4kread
echo "XXX 4kread"
fio --filename=$dev --direct=1 --rw=randrw --refill_buffers --norandommap --randrepeat=0 --ioengine=libaio --bs=8k --rwmixread=70 --iodepth=16 --numjobs=16 --runtime=60 --group_reporting --name=8k7030test
echo "XXX 8k7030test"
fio --filename=$dev --direct=1 --rw=randrw --refill_buffers --norandommap --randrepeat=0 --ioengine=libaio --bs=4k --rwmixwrite=100 --iodepth=16 --numjobs=16 --runtime=60 --group_reporting --name=4kwrite
echo "XXX 4kwrite"
fio --filename=$dev --direct=1 --randrepeat=1 --ioengine=libaio --gtod_reduce=1 --bs=4k --iodepth=64 --size=4G --rw=randrw --rwmixread=70 --name=4k7030thread1
echo "XXX 4k7030thread1"
fio --filename=$dev  --direct=1 --rw=randrw --refill_buffers --norandommap --randrepeat=0 --ioengine=libaio --bs=4k --rwmixread=100 --iodepth=1 --numjobs=1 --runtime=60 --group_reporting --name=4k1thread1queue
echo "XXX 4k1thread1queue"
rm -f $dev
echo "XXX End"
