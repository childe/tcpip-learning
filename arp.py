#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
广播一个ARP请求, 问一下网关的MAC地址是多少.
运行环境是ubuntu12.04.
osx上面是不行的. 据说windows也不行.  搜索了好久, 也不知道mac上面怎么搞.
'''

import socket
import struct


def main():
    st = struct.Struct('!6s 6s h h h b b h 6s 4s 6s 4s')

    GATEWAY = '192.168.1.1'
    MYIP = '192.168.1.8'
    MYMAC = '20:c9:d0:88:96:3f'

    dst_ethernet_addr = ''.join(
        [chr
         (int(e, 16))
         for e in 'FF:FF:FF:FF:FF:FF'.split(':')])
    protocol_type = 0x0806
    hw_addr_space = 1
    protocol_addr_space = 0x800
    hw_addr_length = 6
    protocol_addr_length = 4
    op = 1
    my_mac = ''.join([chr(int(e, 16)) for e in MYMAC.split(':')])
    my_ip = socket.inet_aton(MYIP)
    target_hw_addr = ''.join(
        [chr
         (int(e, 16))
         for e in '00:00:00:00:00:00'.split(':')])
    des_ip = socket.inet_aton(GATEWAY)
    data = (
        dst_ethernet_addr,
        my_mac,
        protocol_type,
        hw_addr_space,
        protocol_addr_space,
        hw_addr_length,
        protocol_addr_length,
        op,
        my_mac,
        my_ip,
        target_hw_addr,
        des_ip,
        )
    packed_data = st.pack(*data)

    s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.SOCK_RAW)
    s.bind(('eth0', socket.SOCK_RAW))
    r = s.send(packed_data)
    print r
    return

if __name__ == '__main__':
    main()
