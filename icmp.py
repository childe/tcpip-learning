#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import gen_checksum
from struct import  pack


def send_icmp(raw_socket, host, icmptype, code, ID, seq, msg):
    ''' raw_socket could be created by:
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    '''
    header = pack('!bbHHH', icmptype, code, 0, ID, seq)
    checksum = gen_checksum(header + msg)
    header = pack('!bbHHH', icmptype, code, checksum, ID, seq)

    raw_socket.sendto(header + msg, (host, 0))
