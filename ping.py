#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import struct
import os
import time
import sys
import signal
import argparse
from icmp import send_icmp

s = None
seq = received = lost = 0


def sumary():
    print
    print '%s packets transmitted, %s packets received, %.2f%% packet loss' % (
        seq, received, 100.0*lost/seq)


def int_handler(signum, frame):
    sumary()
    try:
        s.close()
    finally:
        sys.exit(0)


def ping(host, c=0):
    global s, seq, lost, received

    signal.signal(signal.SIGINT, int_handler)

    pid = os.getpid() & 0xffff

    s = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                      socket.getprotobyname('icmp'))
    s.settimeout(1)

    while c == 0 or seq < c:
        seq += 1
        data = struct.pack('d', time.time()) + 48 * 'Q'
        send_icmp(s, host, 8, 0, pid, seq, data)

        try:
            (content, dst) = s.recvfrom(1024)
        except socket.timeout:
            lost += 1
            print 'Request timeout for icmp_seq', seq
            continue

        ttl, = struct.unpack('!B', content[8:9])
        icmptype, code, checksum, ID, seq = struct.unpack(
            '!bbHHh', content[
                20:20+8])  # 20 IPheader, 8 ICMP header
        if ID != pid:
            continue
        reqtime, = struct.unpack('d', content[28:36])
        received += 1
        restime = time.time()-reqtime
        print '%s bytes from %s: icmp_seq=%s ttl=%s time=%.3f ms' % (len(content)-20,
                                                                     dst[0], seq, ttl, restime*1000)

        time.sleep(1)

    sumary()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", type=int, default=0,help="count")
    parser.add_argument("host")
    args = parser.parse_args(sys.argv[1:])
    ping(args.host, args.c)


if __name__ == '__main__':
    main()
