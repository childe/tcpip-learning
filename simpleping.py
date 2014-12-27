#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import struct
import os
import time
import sys
from icmp import send_icmp


def ping(host):
    pid = os.getpid() & 0xffff
    data = struct.pack('d', time.time()) + 48 * 'Q'

    s = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                      socket.getprotobyname('icmp'))

    send_icmp(s, host, 8, 0, pid, 0, data)

    (content, dst) = s.recvfrom(1024)
    icmptype, code, checksum, ID, seq = struct.unpack(
        '!bbHHh', content[
            20:20+8])  # 20 IPheader, 8 ICMP header
    reqtime, = struct.unpack('d', content[28:36])
    print icmptype, code, checksum, ID, seq, reqtime, time.time()-reqtime


def main():
    ping(sys.argv[1])


if __name__ == '__main__':
    main()
