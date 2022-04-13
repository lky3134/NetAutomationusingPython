#!/bin/env python3
#-*- coding: utf-8 -*-

from history_all import *

def history_usage(history_list):
    cmd_list=[]
    for h in history_list:
        cmd_list.append(h[1])
    
    cmd_key_list= list(set(cmd_list))
    
    cnt_list= [] 
    for cmd in cmd_key_list:
        cnt_list.append(cmd_list.count(cmd))
    
    usage_sort=[]
    i= 0 
    while len(cnt_list) > 0 :
        max_cnt= max(cnt_list)
        max_index= cnt_list.index(max_cnt)
        cmd= cmd_key_list.pop(max_index)
        cnt= cnt_list.pop(max_index)
        usage_sort.append((cmd, cnt))
    return usage_sort

if __name__ == '__main__':
    accouts= get_accounts()
    for account in accouts:
        history_list= history(account)
        
        if len(history_list) == 0:
            print("\t 기록된 이력이 없습니다.  ")
        else:
            usage= history_usage(history_list)
            i=0
            while i < min(3, len(usage)):
                (cmd, cnt) = usage[i]
                if i == 0:
                    print("\t 가장 많이 사용한 명령어 : %s (%d번)" %(cmd, cnt))
                else:
                    print("\t %번째 많이 사용한 명령어 : %s (%d번)" %(cmd, cnt))
                
        print ("-"*70)
        