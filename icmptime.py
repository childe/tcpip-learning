#!/usr/bin/env python
# -*- coding: utf-8 -*-

from icmp import send_icmp
import os
import socket
import sys
import datetime
from struct import pack


def main():
    host = sys.argv[1]
    raw_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_RAW,
        socket.IPPROTO_ICMP)
    pid = os.getpid() & 0xffff
    icmptype = 13  # time request
    code = 0
    seq = 0
    n = datetime.datetime.utcnow()
    microseconds_from_midnight = 1000 * \
        (n.hour*3600+n.minute*60+n.second)+n.microsecond/1000
    msg = pack('I',microseconds_from_midnight)
    send_icmp(raw_socket, host, icmptype, code, pid, seq, msg)


if __name__ == '__main__':
    main()
