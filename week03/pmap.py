# -*- coding:utf8 -*-

import os
import socket
import time
import json
import argparse
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

class PMAP(object):
    def __init__(self, args):
        self.module = args.m
        self.concurrent_num = args.n
        self.method = args.f
        self.ip = args.ip
        self.ip_list = []
        self.result_file = args.w
        self.time_consume = args.v

    def parse_ip(self):
        self.ip_list = []
        ip_list = self.ip.split('-')
        if len(ip_list) == 2: 
            ip_start = ip_list[0].strip()
            ip_end = ip_list[1].strip()
            addr_start = ip_start[ip_start.rfind('.')+1:].strip()
            addr_end = ip_end[ip_end.rfind('.')+1:].strip()
            addr_pre = ip_start[:ip_start.rfind('.')+1]
            addr_len = int(addr_end) - int(addr_start)
            for i in range(addr_len + 1):
                self.ip_list.append(addr_pre + str(int(addr_start) + i))
        else:
            self.ip_list.append(ip_list[0]) 

    def ping_scan(self, ip):
        ping_result = os.popen('ping %s' % ip).read()
        res = 'suc' if 'TTL' in ping_result else 'fail'
        return {'ip': ip, 'ping_result': res}

    def tcp_scan(self, port):
        res = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.settimeout(0.1)
            s.connect((self.ip, port))
            s.shutdown(1)
            print('{}:{} is open'.format(self.ip, port))
            res = True
        except:
            res = False
        finally:
            s.close()
            
        return {'ip': self.ip, 'port': port, 'tcp_result': res}

    def scan(self):
        start = int(time.time())
        Executer = ProcessPoolExecutor if args.m == 'proc' else ThreadPoolExecutor
        with Executer(self.concurrent_num) as executor:
            if self.method == 'ping':
                self.parse_ip()
                exec_result = executor.map(self.ping_scan, self.ip_list)
            else:
                exec_result = executor.map(self.tcp_scan, [port for port in range(1, 65535+1)])
        end = int(time.time())

        if self.time_consume:
            print('time consume: %s' % (end - start))

        scan_result = list()
        for info in exec_result:
            scan_result.append(info)

        if self.result_file:
            with open(self.result_file, 'w') as f:
                f.write(json.dumps(scan_result))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str, choices=['proc', 'thread'], default='proc', help='proc:多进程，thread:多线程')
    parser.add_argument('-n', type=int, choices=[2,3,4], default=2, help='并发数量:2,3,4')
    parser.add_argument('-f', type=str, choices=['ping', 'tcp'], default='ping', help='ping测试，tcp检测')
    parser.add_argument('-ip', type=str, default='14.215.177.39', metavar='ip', help='ip 示例：192.168.0.1 或 192.168.0.1-192.168.0.100')#required=True, 
    parser.add_argument('-w', type=str, default='scan_result.txt', metavar='filename', help='扫描结果保存文件名')
    parser.add_argument('-v', action='store_true', default=True, help='打印扫描器运行耗时')
    args = parser.parse_args()

    pmap = PMAP(args)
    pmap.scan()