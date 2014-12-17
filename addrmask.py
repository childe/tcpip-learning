#!/usr/bin/env python
# -*- coding: utf-8 -*-

from icmp import send_icmp
import os
import socket
import sys


def main():
    host = sys.argv[1]
    raw_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_RAW,
        socket.IPPROTO_ICMP)
    pid = os.getpid()&0xffff
    seq = 0
    send_icmp(raw_socket, host, 17, 0, pid, seq, '00000')


if __name__ == '__main__':
    main()
