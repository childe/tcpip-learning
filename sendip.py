#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''发送一个裸的IP包, 20字节的IP头, 后面跟一个随便写的字符串.
还不知道IP包的ID应该根据什么生成, 就随便写了一个54321
IP头里面:
    IP包总长度属性和checksum属性都是内核自动生成的.
    协议是用的socket.IPPROTO_TCP,也就是6.但没什么用,IP包里面就随便的字符串,不是按TCP协议来的.
'''

import socket
from struct import pack, unpack
import sys

def checksum(ip_header):
    ip_header += chr(0x00)*(len(ip_header)%2)
    r = 0
    while ip_header:
        # 因为ip_header已经是网络序了, 所以这里用!H. 否则需要用H
        r += unpack('!H',ip_header[:2])[0]
        ip_header = ip_header[2:]

    if r > 0xffff:
        r = r&0xffff + (r>>16);

    return ~r


def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except socket.error as msg:
        print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        return

    packet = ''

    source_ip = '127.0.0.1'
    dest_ip = '127.0.0.1'

    # ip header fields
    ip_ver = 4
    ip_ihl = 5
    ip_tos = 0
    ip_tot_len = 0  # kernel will fill the correct total length
    ip_id = 54321
    ip_frag_off = 0
    ip_ttl = 32
    ip_proto = socket.IPPROTO_TCP  # no use in this case
    ip_checksum = 0    # kernel will fill the correct checksum

    ip_saddr = socket.inet_aton(source_ip)
    ip_daddr = socket.inet_aton(dest_ip)

    ip_ihl_ver = (ip_ver << 4) + ip_ihl

    user_data = sys.argv[1] if sys.argv[1:] else '0123456789'

    # this is really not needed, since kernel will give the correct value
    #ip_tot_len = 20 + len(user_data)

    # the ! in the pack format string means network order
    ip_header = pack(
        '!BBHHHBBH4s4s',
        ip_ihl_ver,
        ip_tos,
        ip_tot_len,
        ip_id,
        ip_frag_off,
        ip_ttl,
        ip_proto,
        ip_checksum,
        ip_saddr,
        ip_daddr)


    packet = ip_header + user_data

    # the port specified has no effect
    r = s.sendto(packet, (dest_ip, 0))

    # result is the length of packet sent out
    print r

if __name__ == '__main__':
    main()
