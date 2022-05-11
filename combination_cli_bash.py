#!/bin/env python
#-*- coding: utf-8 -*-

from cli import cli
from subprocess import Popen
from subprocess import PIPE
import datetime
import time
import shutil
import os
import sys

def write_brief(brief_path) :
    ret = cli("show interface brief")
    f = open(brief_path, "w")
    f.write(ret)
    f.close()

def get_diff_data(path1, path2) :
    p = Popen("diff --context %s %s" % (path1, path2), shell=True, stdout=PIPE)
    (ret, err) = p.communicate()

    ret = ret.strip()
    if ret == "" :
        return None
        
    ret = ret.split("***************")[1]
    ret = ret.split("--- ")
    ret_before = ret[0]
    ret_after = ret[1]
    return (ret_before, ret_after)

def get_change_data_list(ret) :
    (ret_before, ret_after) = ret
    before_data_list = []
    for line in ret_before.split("\n") :
        eth_index = line.find("! Eth1")
        if eth_index == 0 :
            eth_num = line.split()[1].split('/')[1]
            before_data_list.append((eth_num, line[2: len(line)]))

    changed_data_list = []
    for (eth_num, before_line)in before_data_list :
        idx = ret_after.find("! Eth1/"+ eth_num)
        enter_idx = ret_after.find("\n", idx)
        after_line = ret_after[idx + 2 : enter_idx]

        changed_data_list.append((eth_num, before_line, after_line))
    return changed_data_list

def print_run_conf(changed_data_list) :
    if len(changed_data_list) == 0 :
        print "변경된 데이터가 없습니다."    

    for (eth_num, before_line, after_line) in changed_data_list :
        print "-" * 10, ("Eth1/%s 정보" % eth_num), "-" * 10
        print "[ 변경 전 인터페이스 간략 정보 ]"
        print "  ", before_line
        print "[ 변경 후 인터페이스 간략 정보 ]"
        print "  ", after_line
        print "[ 현재 인터페이스 구성 정보 ]"
        run_conf = cli("show running-config interface ethernet 1/%s" % eth_num)
        for line in run_conf.split("\n") :
            if line == "" :
                continue
            elif line.startswith("!Command:") or line.startswith("!Time:"):
                continue
            elif line.startswith("version ") :
                continue
            print line
        print "-" * 30    

if __name__ == '__main__':
    term = input("몇 초 단위로 비교하시겠습니까? : ")
    count = input("몇 번 비교하시겠습니까? : ")

    brief_dir = "/bootflash/scripts/tmp"
    if not os.path.isdir(brief_dir) :
        os.mkdir(brief_dir)
        
    cnt = 1
    while cnt <= count :
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(seconds = term)
        now = datetime.datetime.now()

        brief_path1 = "/bootflash/scripts/tmp/brief.txt"
        brief_path2 = "/bootflash/scripts/tmp/brief2.txt"        

        write_brief(brief_path1)
            
        print cnt, "차 비교 중입니다."
        while now <= end_time:
            sys.stdout.write(".")
            sys.stdout.flush()        
            time.sleep(1)
            
            now = datetime.datetime.now()    

        write_brief(brief_path2)

        ret = get_diff_data(brief_path1, brief_path2)
        if ret == None :
            print "\n#### 변경된 정보 출력 (%d 번째) ####" % cnt
            print "변경된 데이터가 없습니다."
            cnt = cnt + 1
            continue
        
        changed_data_list = get_change_data_list(ret)
        
        print "\n#### 변경된 정보 출력 (%d 번째) ####" % cnt
        print_run_conf(changed_data_list)
            
        cnt = cnt + 1

    shutil.rmtree("/bootflash/scripts/tmp")
