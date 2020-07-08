#!/usr/bin/env python
################################################################################
#
# Copyright (C) 2017 Robert Erickson (metaMMAproject@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
import logging
import os
import platform
import random
import re
import time
from datetime import datetime

import event_info
import info_check
import user_info

dic = user_info.dicen

logging.basicConfig(filename=info_check.mma_direct + "log.txt", level=logging.DEBUG,
                    format='[%(asctime)s] %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)
buf = "\n                      "  # buffer space for mult-line log entries
today_date_object = datetime.now()
day_of_week = today_date_object.weekday()


def endit():
    os.remove(info_check.mma_direct + 'meta.running')
    exit()


def exit_stats():
    f = open(info_check.mma_direct + 'stats.txt', 'r')
    filedata = f.read()
    f.close()
    newdata = re.sub(r'.*last time %s successfully exited.' % os.path.basename(__file__), "[" + time.strftime(
        "%Y-%m-%d %H:%M:%S") + "] - last time %s successfully exited." % os.path.basename(__file__), filedata)
    f = open(info_check.mma_direct + 'stats.txt', 'w')
    f.write(newdata)
    f.close()
    endit()


if os.path.isfile(info_check.mma_direct + 'meta.running'):
    log = open(info_check.mma_direct + 'execution-log.txt', 'a')
    log.write("\n[" + time.strftime(
        "%Y-%m-%d %H:%M:%S") + "] An attempt to run meta.py was made." + buf + "However, meta.py is currently running because meta.running is present. The script will stop running now.")
    log.close()
    exit_stats()
else:
    with open(info_check.mma_direct + 'meta.running', "w") as running:
        running.write("[" + time.strftime("%Y-%m-%d %H:%M:%S") + "] meta.py started running.")
        running.close()
    f = open(info_check.mma_direct + 'stats.txt', 'r')
    filedata = f.read()
    f.close()
    newdata = re.sub(r'.*last time meta.py was started.',
                     "[" + time.strftime("%Y-%m-%d %H:%M:%S") + "] - last time meta.py was started.", filedata)
    f = open(info_check.mma_direct + 'stats.txt', 'w')
    f.write(newdata)
    f.close()
if platform.system() == 'Windows' or platform.system() == 'windows':
    os.system("py -3 setup.py")
else:
    os.system("python3 setup.py")

promos_with_events_today = []
promos_without_future_dates = []
far_away = []
f = open(info_check.mma_direct + 'event_dates.txt', "r")
lines = []
for line in f:
    if line.startswith('-----'):
        continue
    date_and_promo = line
    if date_and_promo[-1:] == '\n':
        date_and_promo = date_and_promo[:-1]
    next_wanted_event_date = date_and_promo[:10]
    next_wanted_event_date_object = datetime.strptime(next_wanted_event_date, '%Y-%m-%d')
    dif = (
            next_wanted_event_date_object - today_date_object).days  # number of days until the MMA events that is saved in the event_dates text file
    if next_wanted_event_date != '2050-01-01':
        if dif > 11:
            far_away.append(date_and_promo[11:])
        if dif > -1:
            logger.info(
                "The next scheduled " + date_and_promo[11:] + " event is still " + str(dif + 1) + " days away.")
        else:
            promos_with_events_today.append(date_and_promo[11:])
    else:
        promos_without_future_dates.append(date_and_promo[11:])

waited = 0
if len(
        promos_without_future_dates) > 0:  # Only check wikipedia for new event dates on friday and saturday mornings
    if day_of_week != 4 and day_of_week != 5:
        for z in range(0, len(promos_without_future_dates)):
            logger.info(promos_without_future_dates[
                            z] + " doesn\'t have a future event date stored." + buf + "Will check back on Friday or Saturday for updates.")
    if day_of_week == 4 or day_of_week == 5:
        time.sleep(random.randint(5,
                                  1200))  # Prevent wikipedia from getting slammed at same time every friday/saturday morning
        waited = 1
        try:
            for z in range(0, len(promos_without_future_dates)):
                logger.info(promos_without_future_dates[
                                z] + ' doesn\'t have a future event date stored.' + buf + 'Attempting to find a future event date.')
                event2 = event_info.Event(dic[promos_without_future_dates[z]])
                event2.future('unverified')
        except Exception as e:
            logger.exception(e)
        try:
            for v in range(0, len(far_away)):
                logger.info(far_away[
                                v] + ' event is more than two weeks away.' + buf + 'Checking to see if a new event is happening sooner or the date has been moved up.')
                event3 = event_info.Event(dic[far_away[v]])
                event3.future('unverified')
        except Exception as e:
            logger.exception(e)
if len(promos_with_events_today) < 1:
    logger.info("There are no MMA events taking place today. Exiting script.")
    exit_stats()
else:
    try:
        if waited == 0:
            time.sleep(random.randint(5, 1200))
        for y in range(0, len(promos_with_events_today)):
            logger.info(promos_with_events_today[
                            y] + " has an event taking place today." + buf + "Attempting to find a future event date.")
            event = event_info.Event(dic[promos_with_events_today[y]])
            event.future('verified')
    except Exception as e:
        logger.exception(e)
        endit()
    else:
        exit_stats()
