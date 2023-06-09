from libs.mylogger import logger
from libs.mySelenium import start_google_chrome_with_port, send_keys_and_enter, open_kobetsu_genka
from config import CLOUD_GATE_URL, KOBETSU_GENKA_URL, LOGIN_INFORMATION
from input_kousu import input_kousu

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import datetime
import calendar
import time

if __name__ == '__main__':
    
    input_kousu()