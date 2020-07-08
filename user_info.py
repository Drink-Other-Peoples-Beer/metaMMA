from os import getenv

from dotenv import load_dotenv

load_dotenv()

MMA = int(getenv("MMA"))
MMA_DESTINATION = getenv("MMA_DESTINATION")
UFC = int(getenv("UFC"))
UFC_DESTINATION = getenv("UFC_DESTINATION")
BELLATOR = int(getenv("BELLATOR"))
BEL_DESTINATION = getenv("BEL_DESTINATION")
INVICTA = int(getenv("INVICTA"))
INV_DESTINATION = getenv("INV_DESTINATION")
WSOF = int(getenv("WSOF"))
WSOF_DESTINATION = getenv("WSOF_DESTINATION")
TITAN = int(getenv("TITAN"))
TTN_DESTINATION = getenv("TTN_DESTINATION")
LEGACY = int(getenv("LEGACY"))
LFA_DESTINATION = getenv("LFA_DESTINATION")
ONE = int(getenv("ONE"))
ONE_DESTINATION = getenv("ONE_DESTINATION")
GLORY = int(getenv("GLORY"))
GLR_DESTINATION = getenv("GLR_DESTINATION")
# ______________________________________________________________
TMP_DIR = getenv("TMP_DIR")
DONE_DIR = getenv("DONE_DIR")
REFRESH_PLEX = int(getenv("REFRESH_PLEX"))
PLEX_USERNAME = getenv("PLEX_USERNAME")
PLEX_PASSWORD = getenv("PLEX_PASSWORD")
PLEX_IP = getenv("PLEX_IP")
REFRESH_KODI = int(getenv("REFRESH_KODI"))
MMA_LIB = getenv("MMA_LIB")

DIC = {'INV': "INVICTA", 'BEL': "BELLATOR", 'UFC': "UFC", 'WSOF': "WSOF", 'TTN': "TITAN", 'LFA': "LEGACY",
       'ONE': "ONE", 'GLR': "GLORY"}

dicen = {'Invicta FC': 'INV', 'Bellator': 'BEL', 'UFC': 'UFC', 'WSOF': 'WSOF', 'Titan FC': 'TTN',
         'Legacy Fighting Alliance': 'LFA', 'ONE Championship': 'ONE', 'Glory': 'GLR'}

DATEFORMAT = "%Y-%m-%d %H:%M:%S"

EXECUTION_LOG_FILE = 'execution-log.txt'
EVENT_DATES_FILE = 'event_dates.txt'
STATS_FILE = 'stats.txt'
LOG_FILE = 'log.txt'
