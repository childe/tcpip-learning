#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import unpack

def gen_checksum(msg):
    msg += chr(0x00)*(len(msg) % 2)
    r = 0
    while msg:
        # msg已经是网络序了, 所以这里用H. 否则需要用!H
        r += unpack('H', msg[:2])[0]
        msg = msg[2:]


    while r > 0xffff:
        r = (r & 0xffff) + (r >> 16)

    return (~r) & 0xffff

