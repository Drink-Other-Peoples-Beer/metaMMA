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
import fileinput
import fnmatch
import glob
import logging
import os
import platform
import re
import sys
import time
import urllib
import urllib.request
from datetime import datetime
from shutil import copyfile
from shutil import move

import info_check
import plex_token
import user_info

logging.basicConfig(filename=info_check.mma_direct + "log.txt", level=logging.DEBUG,
                    format='[%(asctime)s] %(message)s', datefmt=user_info.DATEFORMAT)
logger = logging.getLogger(__name__)
buf = "\n                      "  # buffer space for mult-line log entries
dic = user_info.dicen
i_dic = {v: k for k, v in dic.items()}

if info_check.info_updated == 0 or not os.path.exists(info_check.mma_direct):
    exit()


def endit():
    os.remove(info_check.mma_direct + 'mover.running')
    exit()


def exit_stats():
    f = open(info_check.mma_direct + user_info.STATS_FILE, 'r')
    filedata = f.read()
    f.close()
    newdata = re.sub(r'.*last time %s successfully exited.' % os.path.basename(__file__), '[' + time.strftime(
        user_info.DATEFORMAT) + '] - last time %s successfully exited.' % os.path.basename(__file__), filedata)
    f = open(info_check.mma_direct + user_info.STATS_FILE, 'w')
    f.write(newdata)
    f.close()
    endit()


def plex_refresh():
    urllib.request.urlopen(
        'http://localhost:32400/library/sections/' + plex_token.section + '/refresh?X-Plex-Token=' + plex_token.token)


def kodi_refresh():
    if platform.system() == 'Windows' or platform.system() == 'windows':
        os.system("py -3 texturecache.py qax movies @qaperiod=-1 @qa.nfo.refresh=1")
    else:
        os.system("python3 texturecache.py qax movies @qaperiod=-1 @qa.nfo.refresh=1")


def stat_updater(stat_name):
    """
    Args:
        stat_name:
    """
    for line in fileinput.input(info_check.mma_direct + user_info.STATS_FILE):
        temp = sys.stdout
        sys.stdout = open(info_check.mma_direct + 'stats2.txt', 'a')
        if (i_dic[stat_name] in line and 'moved' in line) or ('total' in line and 'moved' in line):
            tmp = re.findall('[0-9]+', line)
            num = str(int(str(tmp[0])) + 1)
            new = re.sub(r'[0-9]+', num, line)
            print(new, end='')
        else:
            print(line, end='')
        sys.stdout.close()
        sys.stdout = temp
    os.remove(info_check.mma_direct + user_info.STATS_FILE)
    os.rename(info_check.mma_direct + 'stats2.txt', info_check.mma_direct + user_info.STATS_FILE)


if os.path.isfile(info_check.mma_direct + 'mover.running'):
    running = open(info_check.mma_direct + 'mover.running', 'r')
    running_script = running.read()
    running.close()
    log = open(info_check.mma_direct + user_info.EXECUTION_LOG_FILE, 'a')
    log.write("\n[" + time.strftime(
        user_info.DATEFORMAT) + "] An attempt to run mover.py was made. However, " + running_script[
                                                                                     22:] + " is currently running. The script will stop running now.")
    log.close()
    exit()
else:
    with open(info_check.mma_direct + 'mover.running', "w") as running:
        running.write("[" + time.strftime(user_info.DATEFORMAT) + "] mover.py")
        running.close()
    f = open(info_check.mma_direct + user_info.STATS_FILE, 'r')
    filedata = f.read()
    f.close()
    newdata = re.sub(r'.*last time mover.py was started.',
                     '[' + time.strftime(user_info.DATEFORMAT) + '] - last time mover.py was started.',
                     filedata)
    f = open(info_check.mma_direct + user_info.STATS_FILE, 'w')
    f.write(newdata)
    f.close()

hour = time.strftime("%H")
hour_int = int(hour)
if 4 < hour_int < 5:
    with open(info_check.mma_direct + user_info.LOG_FILE, 'r') as myfile:
        earliest_date = myfile.read()[1:20]
        myfile.close()
    earliest_date_object = datetime.strptime(earliest_date, '%Y-%m-%d %H:%M:%S')
    current_date_object = datetime.now()
    time_dif = current_date_object - earliest_date_object
    second_dif = time_dif.total_seconds()
    if (second_dif > 1814400):  # if the current log.txt file has over 3 weeks of logs then proceed
        previous_log_holder_list = glob.glob(
            info_check.mma_direct + 'previous-log.txt')  # check to see if the "previous-log.txt" file exists
        if len(previous_log_holder_list) == 1:
            os.remove(info_check.mma_direct + 'previous-log.txt')
        move(info_check.mma_direct + user_info.LOG_FILE, info_check.mma_direct + 'previous-log.txt')
        filename = info_check.mma_direct + "log.txt"
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(filename, "w") as log:
            log.write("[" + time.strftime(
                user_info.DATEFORMAT) + "] New log.txt file created. For the previous 3 weeks of logs, open previous-log.txt.")
            log.close()

video_holder_filename = []  # this list will contain all the "holder" filenames that are waiting for a video file to replace them
video_holder_path = []  # this list will contain the path to the "holder" files
video_holder_path_and_file = []  # this list contains the whole path and filname of the "holder" file (will be used to delete the holder file after the video file that is replacing it is moved)

for root, dirnames, filenames in os.walk(
        user_info.MMA_DESTINATION):  # this directory is where all new events directories will be created
    for filename in fnmatch.filter(filenames,
                                   '*.avi'):  # look for all 'holder' files that were created with each new event directory
        video_holder_path_and_file.append(os.path.join(root, filename))
        video_holder_path.append(root)
        h_filename = open(os.path.join(root, filename), 'r').read()
        video_holder_filename.append(h_filename)
if len(video_holder_path) < 1:
    #    logger.info("There were no holder files in the destination directory, therefore no files to look for. The script will stop running now.")
    exit_stats()

badwords = ['weigh-i[a-z]+', 'dana', 'post.fight', '720p', 'webrip', 'breakdown', 'the.fly', 'inside', 'road',
            'history', 'vlog', 'now', 'countdown', 'h264', 'x264', 'press.conference', 'greatest.fighters']
big_regex = re.compile('|'.join(badwords))

for x in range(0, len(video_holder_filename)):
    holder_search_terms1 = video_holder_filename[x].lower()
    holder_search_terms = holder_search_terms1.split()
    completed_video_path_and_filename = []
    completed_video_filename = []
    for root, dirnames, filenames in os.walk(
            user_info.done_dir):  # this is the directory that the completed video files are moved to. MUST BE ON SAME DRIVE AS DOWNLOAD DIRECTORY
        for filename in fnmatch.filter(filenames,
                                       '*[m|M][k|K|p|P][v|V|4]'):  # search for video files ending in "mp4" or "mkv"
            completed_video_path_and_filename.append(os.path.join(root, filename))
            completed_video_filename.append(filename)
    for y in range(0, len(completed_video_path_and_filename)):
        completed_video_name_lower = completed_video_filename[y].lower()
        completed_video_name_no_spaces = completed_video_name_lower.replace(" ", ".")
        completed_video_name_no_leading_s = re.sub(r's(?=[0-9][0-9])', '',
                                                   completed_video_name_no_spaces)  # This is for files like 'The Ultimate Fighter S25 Finale.mp4'
        complete_video_name_early_fix = re.sub(r'[E|e].?[R|r][L|l][Y|y]', r'early',
                                               completed_video_name_no_leading_s)  # replaces "Erly" typo that is common with "early" to standardize
        completed_video_name_prelim_fixed = re.sub(r'[P|p][R|r][E|e][L|l][I|i][a-zA-Z]+', r'prelim',
                                                   complete_video_name_early_fix)  # replaces any version of "PRELIMINARY/prelims" with "prelim" to standardize the search term
        fix = big_regex.sub('', completed_video_name_prelim_fixed)  # removes all prohibited words from filename
        fix2 = re.sub(r'\.+', ' ', fix)  # replaced all dots left after removing prohibited words
        fix3 = fix2.lstrip()  # strips a leading whitespace, if the filename started with a prohibited word
        video_name_search_terms = fix3.rsplit(" ")
        video_name_search_terms = ['lfa' if x == 'legacy' else x for x in video_name_search_terms]
        if set(video_name_search_terms).issuperset(holder_search_terms):
            if 'mkv' in video_name_search_terms:
                v_end = '.mkv'
            else:
                v_end = '.mp4'
            if set(holder_search_terms).issuperset(['bellator']):
                stat_name = 'bel'
            elif set(holder_search_terms).issuperset(['invicta', 'fc']):
                stat_name = 'inv'
            elif set(holder_search_terms).issuperset(['one', 'championship']):
                stat_name = 'one'
            elif set(holder_search_terms).issuperset(['glory']):
                stat_name = 'glr'
            elif set(holder_search_terms).issuperset(['titan', 'fc']):
                stat_name = 'ttn'
            elif set(holder_search_terms).issuperset(['wsof']):
                stat_name = 'wsof'
            elif set(holder_search_terms).issuperset(['lfa']):
                stat_name = 'lfa'
            else:
                stat_name = 'ufc'
            dest_direct = os.path.join(video_holder_path[x], '')
            event_direct = dest_direct[:-11]
            title = 'not-main'
            matched = 0
            if ('early' in video_name_search_terms) and ('early' in holder_search_terms):
                v_end = 'Early Prelims' + v_end
                matched = 1
            elif ('prelim' in video_name_search_terms) and ('prelim' in holder_search_terms) and (
                    'early' not in video_name_search_terms) and ('early' not in holder_search_terms):
                v_end = 'Prelims' + v_end
                matched = 1
            elif ('bellator' in video_name_search_terms) and ('bellator' in holder_search_terms) and (
                    'kickboxing' in video_name_search_terms) and ('kickboxing' in holder_search_terms):
                v_end = 'Bellator Kickboxing' + v_end
                matched = 1
            elif ('early' not in video_name_search_terms) and ('prelim' not in video_name_search_terms) and (
                    'early' not in holder_search_terms) and ('prelim' not in holder_search_terms):
                title = os.path.basename(os.path.normpath(video_holder_path[x]))
                v_end = title + v_end
                event_direct = os.path.join(video_holder_path[x], '')
                matched = 1
            if matched == 1:
                logger.info("Video found at" + buf + completed_video_path_and_filename[
                    y] + buf + "will be copied to" + buf + dest_direct + v_end + buf + "and" + buf +
                            video_holder_path_and_file[x] + buf + "will be deleted.")
                copyfile(completed_video_path_and_filename[y], dest_direct + v_end)
                stat_updater(stat_name)
                os.remove(video_holder_path_and_file[x])
                if title != 'not-main':
                    logger.info("Poster will be renamed to match recently moved Main Card video file.")
                    for basename in os.listdir(video_holder_path[x]):
                        if basename.endswith('.jpg'):
                            pathname = os.path.join(video_holder_path[x], basename)
                            if os.path.isfile(pathname):
                                move(pathname, event_direct + title + ".jpg")
                    logger.info(
                        "nfo file will be updated, and \"Soon - \" will be removed from before the title.")
                    old_nfo = open(event_direct + title + '.nfo', 'r')
                    new_nfo = open(event_direct + title + '2.nfo', 'w')
                    for line in old_nfo:
                        new_nfo.write(line.replace('Soon - ', ''))
                    old_nfo.close()
                    new_nfo.close()
                    os.remove(event_direct + title + '.nfo')
                    move(event_direct + title + '2.nfo', event_direct + title + '.nfo')
                if user_info.refresh_plex == 1:
                    logger.info(
                        "Directory" + buf + event_direct + buf + "will be moved to " + buf + user_info.tmp_dir + buf + "to aid in refreshing.")
                    move(event_direct, user_info.tmp_dir)
                    time.sleep(5)
                    plex_refresh()
                    time.sleep(25)
                    logger.info("Directories and files will be moved back to" + buf + os.path.abspath(
                        os.path.join(event_direct,
                                     os.pardir)) + buf + "in order to help refresh. The script will stop running now.")
                    for node in os.listdir(user_info.tmp_dir):
                        if not os.path.isdir(node):
                            move(os.path.join(user_info.tmp_dir, node),
                                 os.path.join(os.path.abspath(os.path.join(event_direct, os.pardir)), node))
                    plex_refresh()
                if user_info.refresh_kodi == 1: kodi_refresh()
                exit_stats()

# logger.info("There were holder files in the destination directory, but there were no matching video files in your source directory. The script will stop running now.")
exit_stats()
