from hanziconv import HanziConv
from zhon import hanzi
import string
punctuation=hanzi.punctuation + string.punctuation
punctuation = set([i for i in punctuation])

def remove_punctuation(x):  # 删除标点
    x = "".join([i for i in x if i not in punctuation]) # 遍历评论每个字符，若是标点，去掉，用空字符连接
    return re.sub(r'\s+', ' ', x) # 把 x 通过正则表达式 (\s 代表空格，+ 代表多个)，替换成 空字符

# download 数字化
import re
def get_download(x):
    if x == "":
        return 0
    elif '万'in x:
        return int(re.findall(r'\d+', x)[0] + '0000')
    elif '亿'in x:
        return int(re.findall(r'\d+', x)[0] + '00000000')  # 这样计算是有误差的,比如 6.9亿  r'\d+\.\d+' 来匹配，但是转换为整数要分步骤
    else:
        return int(re.findall(r'\d+', x)[0])

# 时间戳 转 时间
import time
def get_download_time(x):
    tl = time.localtime(int(x))
    return time.strftime("%Y-%m-%d %H:%M:%S", tl) 

# taptap 十分制
def format_score(df):
    if df.source == 'taptap':
        return df.score/2
    else:
        return df.score

# 时间差
import datetime
now_time = datetime.datetime.now()
def get_mistiming(x):
    comment_time = datetime.datetime.utcfromtimestamp(int(x))
    return (now_time - comment_time).days