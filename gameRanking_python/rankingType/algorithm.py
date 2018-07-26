# 计算 贝叶斯平均 好评的平均程度
def get_average_comment(df, *args):
    average_total = args[0]
    average_score = args[1]
    return (df.sum_total * df.format_score + average_total * average_score) /(df.sum_total + average_total) 

# 综合热度
import math
def get_compre(df):
    a = math.log(10, df.download_sum_num + 1) * 4 + (df.sum_total * df.format_score)/5
    b = math.pow(df.days_diff_today * 24/2, 1.5) + 1   #次方
    return a/b
