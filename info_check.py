#!/usr/bin/env python3
import os
from pathlib import PurePath

import user_info

dic = user_info.DIC
info_updated = 0
promolist = []
for k, v in dic.items():
    if eval('user_info.' + v) == 1:  # create list of promotions that need metadata scrape
        promolist.append(k)
if user_info.MMA_DESTINATION == '/media/QQQ/MMA/':
    print('Please update the MMA destination directory.')
    exit()
elif user_info.MMA != 1:
    for x in range(0, len(
            promolist)):  # if all promotions will have different destination directories, make sure they are specified
        if eval('user_info.' + promolist[x] + '_DESTINATION') == os.path.join('/media/QQQ/' + dic[promolist[x]],
                                                                              ''):
            print('Please update the ' + dic[promolist[x]] + ' destination directory.')
            exit()
        elif PurePath(user_info.MMA_DESTINATION) not in PurePath(
                eval('user_info.' + promolist[x] + '_DESTINATION')).parents:
            print(user_info.MMA_DESTINATION + ' must be the parent directory of ' + eval(
                'user_info.' + promolist[x] + '_DESTINATION'))
            exit()
elif user_info.REFRESH_PLEX > 1:
    print('Please choose \'1\' or \'0\' for \'refresh_plex\'')
    exit()
elif user_info.REFRESH_KODI > 1:
    print('Please choose \'1\' or \'0\' for \'refresh_kodi\'')
    exit()
elif (user_info.TMP_DIR == '/media/QQQ/tmp/'):
    print('Please update the temporary directory.')
    exit()
elif (user_info.DONE_DIR == '/media/QQQ/done/'):
    print('Please update the the video source directory.')
    exit()
if user_info.REFRESH_KODI == 1:
    if not os.path.isfile(os.path.join(os.path.expanduser("~"), "") + 'texturecache.py'):
        print('Please install \'texturecache.py\' in order to refresh KODI.')
        exit()
if user_info.REFRESH_PLEX == 1:
    if (user_info.MMA_LIB == 'QQQ'):
        print('Please update the name of the pleX library that scans for MMA videos.')
        exit()
    elif (user_info.PLEX_USERNAME == 'QQQ'):
        print('Please update your plex username.')
        exit()
    elif (user_info.PLEX_PASSWORD == 'QQQ'):
        print('Please update your plex password.')
        exit()
    elif (user_info.PLEX_IP == '192.168.QQQ.QQQ'):
        print('Please update the ip address of the machine running the pleX media server software.')
        exit()
home = os.path.join(os.getcwd(), "")
mma_direct = os.path.join(os.path.join(home, ".MMA"), "")
meta = home
info_updated = 1
