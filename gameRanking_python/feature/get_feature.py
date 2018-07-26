from utils import db
from pretreatment import pre_treat
def f_downlaod():
    """
    
    """
    # 从 s_game_detail 获取数据
    sql = "SELECT source, game_name, game_logo_url, score,comments, tags, updated_at, download FROM s_game_detail"
    df_game_download = db.get_df(sql, db='game_source')
    
    # 去掉 空字符
    df_game_download = df_game_download[~(df_game_download['download'] == "")]
    df0 = df_game_download

    # dowanload 数字化
    df_game_download['download_num'] = df_game_download['download'].apply(pre_treat.get_download)

    # game_format_name
    df_game_download['game_format_name'] = df_game_download['game_name'].apply(pre_treat.remove_punctuation)

    # 找出每个游戏 最新更新 的download
    df_download_num = df_game_download.groupby(['game_format_name','source'])['download_num'].max().reset_index()  #reset_index() 不能缺

    # 计算游戏A 全渠道 最新 下载数量之和
    df_download_num = df_download_num.groupby(['game_format_name'])['download_num'].sum().reset_index()
    df_download_num.columns = ['game_format_name', 'download_sum_num'] 

    # 获得 游戏下载指标
    df_detail = df0.merge(df_download_num, how='left', on='game_format_name').reset_index()
    return df_detail

def f_comments():
    # 从 s_game_comment_number 取评论数
    sql = "SELECT * FROM s_game_comment_number"
    df_game_comment = db.get_df(sql, db='game_source')

    # total非空, 转整型
    df_game_comment =df_game_comment[~(df_game_comment['total'].isin(['']))]
    df_game_comment['total'] = df_game_comment['total'].astype('int32')
 
    # foramt game name
    df_game_comment['game_format_name'] = df_game_comment['game_name'].apply(pre_treat.remove_punctuation)
    
    # game A 各source 评论数量
    df_max_total = df_game_comment.groupby(['game_format_name','source'])['total'].max().reset_index()
    df_sum_total = df_max_total.groupby(['game_format_name'])['total'].sum().reset_index()
    df_sum_total.columns = ['game_format_name','sum_total']
    
    # sum_total >1000
    df_sum_total = df_sum_total[df_sum_total['sum_total'] > 1000]
    return df_sum_total

def f_time():
    # time
    sql = "SELECT source, game_name, comment_time, updated_at FROM s_game_comments_taptap_game"
    df_game_time = db.get_df(sql, db='game_source')
   
    # 去空值
    df_game_time = df_game_time[~(df_game_time['comment_time'] == "")]

    # 获得最小评论时间
    df_mix_comment = df_game_time.groupby(['game_name'])['comment_time'].min().reset_index()
    
    # format
    df_mix_comment['comment_format_time'] = df_mix_comment['comment_time'].apply(pre_treat.get_download_time)
    df_mix_comment['game_format_name'] = df_mix_comment['game_name'].apply(pre_treat.remove_punctuation)
    return df_mix_comment[['game_format_name','comment_time']]
    