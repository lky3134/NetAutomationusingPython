#!/bin/env python3
#-*- coding: utf-8 -*-

from history_all import *

if __name__ == '__main__':
    accouts= get_accounts()
    for account in accouts:
        history_list= history(account)
        
        newest_cnt= min(5, len(history_list))
        
        if newest_cnt == 0:
            print("\t 기록된 이력이 없습니다.  ")
            
        i=0
        while i < newest_cnt:
            print("\t %s %s" %s history_list[i])
            i= i+1
        print ("-"*70)
        