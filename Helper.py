import csv, time
import subprocess, os
import pandas as pd

import datetime
import telegram

def telegram_notify(content, status):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = 'Time: {}\n' \
           'Name: {}\n' \
           'Status: {}\n'.format(date, content, status)

    bot_token = '1611170552:AAGSC_PtOlsEy5fUuZ_2u7wDScW3cUtLaX0'
    chat_id = 680568042

    expr_bot = telegram.Bot(token=bot_token)
    expr_bot.send_message(chat_id=chat_id, text=text)

def joinList(li, joinStr='\n', func=str):
    return joinStr.join([func(i) for i in li]) 

def joinLL(lists, joinStrWord=' ', joinStrLine='\n', func=str):
    listStrs = [joinList(li, joinStrWord, func) for li in lists]
    return joinList(listStrs, joinStrLine, func) 

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def calc_accuracy(df_codes:pd.DataFrame, column:str, nullCheck=False) -> (int, int, float):
    if nullCheck:
        num = len(df_codes[~pd.isnull(df_codes[column])])
    else:
        num = len(df_codes[df_codes[column] == 1])
    den = len(df_codes)
    return (num, den, round(100* num/den, 2))

def readCSV(fname):
    f = open(fname, 'rU')
    freader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    lines = list(freader)
    f.close()
    headers = [i.strip() for i in lines[0]]

    return headers, lines[1:]

def writeCSV(fname, headers, lines):    
    fwriter = csv.writer(open(fname, 'w'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)    
    fwriter.writerow(headers)
    fwriter.writerows(lines)

def writeDF_excel(df, fname):
    df.to_excel(fname, encoding = "ISO-8859-1", engine='xlsxwriter')

def write_file(fname, text):
    file = open(fname, 'w')
    file.write(text)
    file.close()

def del_file(fname):
    if os.path.exists(fname):
        os.remove(fname)

def read_file(fname):
    file = open(fname, 'r')
    file.readlines()
    return file

def subprocess_run(cmd_list, prog_input=None, blame_str='subprocess', timeout=5, debug=False, raiseExp=True):
    # Run cmd_list
    proc = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    try:
        if prog_input is None:
            outs, errs = proc.communicate(timeout=timeout)
        else:
            outs, errs = proc.communicate(input=str(prog_input).encode(), timeout=timeout)

    except subprocess.TimeoutExpired:
        # Timeout?
        proc.kill()
        if raiseExp:
            raise Exception('{}: Timeout'.format(blame_str))
        return False, ''

    # Failure?
    if proc.returncode != 0:
        if not debug:  # If not running in debug
            errs = 'Failure'  # fail with a simple "failure" msg

        if raiseExp:
            raise Exception('{}: {}'.format(blame_str, errs))

    return proc.returncode == 0, outs.decode()


def removeDuplicates(li):
    seen = {}
    uniqLi = []

    for item in li:
        if item not in seen:
            uniqLi.append(item) 
            seen[item] = 1
            
    return uniqLi

class MaxTimeBreak:
    def __init__(self, maxTime):
        self.maxTime = maxTime
        self.startTime = time.time()
        self.endTime = self.startTime + self.maxTime
        self.timesUp = False

    def isTimeUp(self):
        currTime = time.time()
        if currTime >= self.endTime:
            self.timesUp = True
            return True
        return False
