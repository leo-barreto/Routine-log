#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from datetime import date, timedelta, datetime
from matplotlib import pyplot as plt


TD = datetime.today()
CODE = {'S': 'Sono', 'P': 'Projeto', 'G': 'Game'}
LOG = 'log.txt'
CAT = 'categories.txt'


def ReadLog(txt = LOG):
    log = np.genfromtxt(txt, dtype = 'str', delimiter = ';')
    return log


def AddEntry(arg, txt = 'log.txt'):
    titles = ['Date: ', 'Start: ', 'End: ', 'Desc: ', 'Cats: ']
    
    if arg[0].find('+') != -1:
        d = int(arg[0][1:])
        day = TD + timedelta(days = d) 
        
    else:
        d = int(arg[0])
        day = date(TD.year, TD.month, d)
    
    arg[0] = str(day).split()[0]
        
    f = open(txt, 'a')
    for i in range(len(titles)):
        f.write(arg[i] + '\t')
        print('\t' + titles[i] + arg[i])
        
    f.write('\n')
    f.close()


#def Categories(txt = CAT):
#     = np.genfromtxt(txt, dtype = 'str')
    
def AnalysisHours(log, start, end, PLOT = True):
    catlog = ReadLog(CAT)
    N = range(len(catlog))
    ct, cl, dc = catlog[:, 0], catlog[:, 1], catlog[:, 2]
        
    hours = np.zeros(len(catlog))
    
    for entry in log:
        t1 = entry[0] + entry[1]
        t2 = entry[0] + entry[2]
        cat = entry[4]
        
        T1 = datetime.strptime(t1, '%Y-%m-%d%H%M')
        T2 = datetime.strptime(t2, '%Y-%m-%d%H%M')
        
        if start <= T1 and T2 <= end:
            for i in N:
                if cat == ct[i]:
                    diff = (T2 - T1).total_seconds() / 3600
                    if diff < 0:
                        diff += 24
                    hours[i] += diff
    
    dt = (end - start).total_seconds() / 3600
    h2, cl2, dc2 = [], [], []    # Only non-0 hours categories
        
    for i in N:
        cl[i] = '#' + cl[i] 
        v = hours[i]
        if v != 0:
            h2.append(v)
            cl2.append(cl[i])
            dc2.append(dc[i])
            relv = 100 * v / dt
            print('{0}: {1}h ({2:.1f}%)'.format(dc[i], v, relv))
            
        
    if PLOT:
        explode = np.zeros(len(h2))
        plt.pie(h2, explode, dc2, cl2)
        plt.suptitle('Hours Proportion', fontsize = 16)
        plt.title(start.strftime('%d/%m/%y') + ' - ' + end.strftime('%d/%m/%y'))
        plt.axis('equal')
        plt.show()

    
    
    

# Commands
while True:
    command = input('$ ').split()
    c = command[0]
    arg = command[1:]
    
    if c == 'ae':
        AddEntry(arg)
        
    elif c == 'rl':
        ReadLog()
    
    elif c == 'help':
        print('heeelp')
        
    elif c == 'q': # quit
        break
    
    elif c == 'anh': 
        en = TD
        if arg[0] == 'ld':
            st = TD - timedelta(days = 1)
        elif arg[0] == 'lw':
            st = TD - timedelta(days = 7)
        elif arg[0] == 'lm':
            st = TD - timedelta(days = 30)
        elif arg[0] == 'ly':
            st = TD - timedelta(days = 365)
        else:
            st = datetime.strptime(arg[0], '%Y-%m-%d')
            en = datetime.strptime(arg[1], '%Y-%m-%d')
            
        AnalysisHours(ReadLog(), st, en)
        
    else:
        print('Invalid command. Check "help".')
