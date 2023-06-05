import libs.mylogger

import glob
import json
import pathlib

CLOUD_GATE_URL = r'https://echizen.cloudgate.jp/user-hub/yachiyo-ind/'

GMAIL_URL = r'https://mail.google.com/a/yachiyo-ind.co.jp/'

CALENDAR_URL = r'https://calendar.google.com/calendar/u/0/r?tab=mc&pli=1'

KOBETSU_GENKA_URL = r'https://echizen.cloudgate.jp/sso/yachiyo-ind/post.xhtml?providerUuid=284c5466-7256-49e3-99ab-04ff1a8178a8'

KINTAIKANRI_URL = r'https://yachiyo-ind.obic7.obicnet.ne.jp/Obic7FederationService'

GUEST_WIFI_URL = r'https://sites.google.com/yachiyo-ind.co.jp/yachiyo-portal/guest-wifi'

newWindosList = {
    # GMAIL_URL: '#\:mr > div > div > a',
    # CALENDAR_URL: 'body',
    KOBETSU_GENKA_URL: 'body',
    # KINTAIKANRI_URL: 'body',
}

ROOT_PATH = pathlib.Path(__file__).parents[1]
try:
    with open(glob.glob(f'{ROOT_PATH}/*.json')[0]) as f:
        LOGIN_INFORMATION = json.load(f)
except FileNotFoundError as e:
    print(e)
    
if __name__ == '__main__':
    # log
    libs.mylogger.logger.info(f'ROOT_PATH path : {ROOT_PATH}')
    libs.mylogger.logger.info(f'CLOUD_GATE_URL : {CLOUD_GATE_URL}')
    libs.mylogger.logger.info(f'KOBETSU_GENKA_URL : {KOBETSU_GENKA_URL}')