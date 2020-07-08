from os import getenv

from dotenv import load_dotenv

load_dotenv()

MMA = getenv("MMA")
MMA_DESTINATION = getenv("MMA_DESTINATION")
UFC = getenv("UFC")
UFC_DESTINATION = getenv("UFC_DESTINATION")
BELLATOR = getenv("BELLATOR")
BEL_DESTINATION = getenv("BEL_DESTINATION")
INVICTA = getenv("INVICTA")
INV_DESTINATION = getenv("INV_DESTINATION")
WSOF = getenv("WSOF")
WSOF_DESTINATION = getenv("WSOF_DESTINATION")
TITAN = getenv("TITAN")
TTN_DESTINATION = getenv("TTN_DESTINATION")
LEGACY = getenv("LEGACY")
LFA_DESTINATION = getenv("LFA_DESTINATION")
ONE = getenv("ONE")
ONE_DESTINATION = getenv("ONE_DESTINATION")
GLORY = getenv("GLORY")
GLR_DESTINATION = getenv("GLR_DESTINATION")
# ______________________________________________________________
TMP_DIR = getenv("TMP_DIR")
DONE_DIR = getenv("DONE_DIR")
REFRESH_PLEX = getenv("REFRESH_PLEX")
PLEX_USERNAME = getenv("PLEX_USERNAME")
PLEX_PASSWORD = getenv("PLEX_PASSWORD")
PLEX_IP = getenv("PLEX_IP")
REFRESH_KODI = getenv("REFRESH_KODI", 0)
MMA_LIB = getenv("MMA_LIB")
