#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import http.client as client
import urllib.request as request

import user_info


class PlexToken:
    BASE_64_STRING = base64.encodebytes(
        ('%s:%s' % (user_info.PLEX_USERNAME, user_info.PLEX_PASSWORD)).encode()
    ).decode().replace('\n', '')
    TX_DATA = ""

    headers = {'Authorization': "Basic %s" % BASE_64_STRING,
               'X-Plex-Client-Identifier': "MMA script",
               'X-Plex-Product': "MMA script 356546545",
               'X-Plex-Version': "0.001"}

    CONN = client.HTTPSConnection("plex.tv")
    CONN.request("POST", "/users/sign_in.json", TX_DATA, headers)
    response = CONN.getresponse()
    data = response.read()
    DATA_STR = str(data)
    token_str_plus = DATA_STR.split('_token":"')[1]
    token_str = token_str_plus.split('"')[0]
    token = token_str
    CONN.close()

    section_info_xml = request.urlopen(
        'http://' + user_info.PLEX_IP + ':32400/library/sections/?X-Plex-Token=' + token_str
    ).read().decode('utf-8')

    section_info_plus2 = section_info_xml.split(user_info.MMA_LIB)[0]
    section_info_plus = section_info_plus2.rsplit('key="', 1)[1]
    section_str = section_info_plus.split('"')[0]
    section = section_str
