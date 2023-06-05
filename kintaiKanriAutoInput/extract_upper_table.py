from libs.mylogger import logger
from libs.mySelenium import start_google_chrome_with_port, send_keys_and_enter, open_kobetsu_genka
from config import CLOUD_GATE_URL, KOBETSU_GENKA_URL, LOGIN_INFORMATION

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import datetime
import calendar
import time


def extact_daily_total(driver, rowNum):
    '''上段テーブルを取得'''
    
    get_table = []
    css = f'#tblDayTotal > tbody > tr:nth-child({rowNum}) > td'
    for ele in driver.find_elements(By.CSS_SELECTOR, css):
        txt = ele.text
        if txt == '':
            get_table.append(0.0)
        else:
            get_table.append(txt)
            
    return get_table

    
def create_Operationtime_tabel(driver, actionChains):
    '''入力工数のテーブルを作成'''
    
    get_tables = []
    for rowNum in range(5):
        get_table = extact_daily_total(driver, rowNum+1)
        get_tables.append(get_table)
        logger.debug(get_table)
    
    # 日付のインデックスを作成
    today = datetime.date.today()
    firstDate = today.replace(day=1)
    lastDate = today.replace(day=calendar.monthrange(today.year, today.month)[1])
    date_index = pd.date_range(start=firstDate, end=lastDate, freq="d")

    # DataFrame整列
    initial_df = pd.DataFrame(get_tables).T
    initial_df.columns = list(initial_df.iloc[0])
    df = initial_df.drop(index=initial_df.index[[0, 1]])
    df = df.drop(columns=initial_df.columns[-1], axis=1)
    df = df.astype(float)
    df = df.set_index(date_index)
    df.head(2)

    # 工数テーブルの作成
    # 不稼働表示 'YRD-0', 'YRD-1', 'YRD-2', 'YRD-3', 'YRD-4'
    mainOperationtime = 4.0
    downtime = 1.0
    df['KP01YRSX02'] = mainOperationtime
    df['KP02YRSX02'] = (df['勤怠工数'] - mainOperationtime - downtime).round()

    for i, label in enumerate(['YRD-0', 'YRD-1', 'YRD-2', 'YRD-3', 'YRD-4']):
        df.loc[df.index.weekday == i, label] = downtime

    df.loc[df.index.weekday == 5, ['KP01YRSX02', 'KP02YRSX02']] = 0
    df.loc[df.index.weekday == 6, ['KP01YRSX02', 'KP02YRSX02']] = 0

    df.fillna(0, inplace=True)
    df.head(6)

    # 昨日までのデータを入力
    df_yesterday = df[df.index < today.strftime('%Y%m%d')]

    for x, index in enumerate(df_yesterday.index):
        for y, column in enumerate(df_yesterday.iloc[x, 4:]):
            css = f'#divTblProductCostInfo > div > div > div > div > table > tbody > tr:nth-child({1+y}) > td:nth-child({14+x})'
            ele = driver.find_element(By.CSS_SELECTOR, css)
            actionChains.click(ele).perform()
            actionChains.send_keys(Keys.BACKSPACE).perform()
            actionChains.send_keys(f'{column}').perform()


def input_yes_or_no(driver):
    '''yes noで登録判断'''
    
    ynDict={'y':True,'yes':True,'n':False,'no':False}
    logger.info('Would you like to register?')
    
    if ynDict[input('[Y]es/[N]o? >> ').lower()]:
        driver.find_elements(By.CSS_SELECTOR, '#btnReg')[0].click()
        time.sleep(0.5)
        driver.find_elements(By.CSS_SELECTOR, 'button.swal2-confirm.swal2-styled')[0].click()
        time.sleep(0.5)
        driver.find_elements(By.CSS_SELECTOR, 'button.swal2-confirm.swal2-styled')[0].click()
    else:
        logger.info('Please register after confirmation.')
        pass
    logger.info('Exit the program.')


##### main #####

def extract_upper_tabel():
    
    driver, actionChains = start_google_chrome_with_port(CLOUD_GATE_URL)
    try:
        send_keys_and_enter(driver, LOGIN_INFORMATION, '#rawUsername', 'ID')
        send_keys_and_enter(driver, LOGIN_INFORMATION, '#password', 'PASSWORD')
    except:
        pass

    open_kobetsu_genka(
        driver=driver,
        url=KOBETSU_GENKA_URL,
        css='body', winNum=1)

    # 日別合計
    create_Operationtime_tabel(driver, actionChains)
        
    # 登録判断
    input_yes_or_no(driver)



if __name__ == '__main__':
    extract_upper_tabel()