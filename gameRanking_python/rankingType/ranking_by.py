from utils import db
from pretreatment import pre_treat
from . import algorithm
def by_download(df):
    # 获取下载榜
    df_download = df.drop_duplicates(['game_format_name'])
    df_ranking_by_download = df_download.sort_values(by=['download_sum_num'], ascending=False).reset_index()
    
    # 下载榜 写入 s_lcs_game_ranking_by_download
    db.write_to_mysql(df_ranking_by_download, db='game_process', tb="s_lcs_game_ranking_by_download_python", type='replace', index=True)

def by_comments(df):
    # 获取 热门榜
    df_total = df.drop_duplicates(['game_format_name'])
    df_ranking_by_total = df_total.sort_values(by=['sum_total'], ascending=False).reset_index()
    # 下载榜 写入 s_lcs_game_ranking_by_total
    db.write_to_mysql(df_ranking_by_total, db='game_process', tb="s_lcs_game_ranking_by_total_python", type='replace', index=True)


def by_time(df):
    # 获取 新游榜
    df_time = df.drop_duplicates(['game_format_name'])
   
    # nan
    df_time = df_time.fillna(0)
    df_time['comment_time'] = df_time['comment_time'].astype('int32')
    df_time = df_time[~(df_time['comment_time'] == 0)]
   
    # 70天之内的游戏
    df_time['days_diff_today'] = df_time['comment_time'].apply(pre_treat.get_mistiming)
    df_time_300 = df_time[df_time['days_diff_today'] < 70]
    
    # 新游戏 ranking by downlaod
    df_ranking_by_time = df_time_300.sort_values(by=['download_sum_num'], ascending=False)
   
    # 下载榜 写入 s_lcs_game_ranking_by_time
    db.write_to_mysql(df_ranking_by_time, db='game_process', tb="s_lcs_game_ranking_by_time_python", type='replace', index=True)

def by_score(df):
    # 评分榜 考虑好评的平均程度
    df_score = df.drop_duplicates(['game_format_name'])
    
    # score total=0 是 fillna 来的
    df_score_0 = df_score[df_score['sum_total'] > 0]
    df_score_total_0 = df_score_0[df_score_0['score'] > 0]
    
    # format_score  taptap 十分制
    df_score_total_0['format_score'] = df_score_total_0.apply(pre_treat.format_score, axis=1)
    
    # average_total   average_score
    average_total = df_score_total_0['sum_total'].sum() / len(df_score_total_0)
    average_score = df_score_total_0['format_score'].sum() / len(df_score_total_0)
    
    # 计算贝叶斯平均 好评的平均程度 指标为
    df_score_total_0['average_comment'] = df_score_total_0.apply(algorithm.get_average_comment, axis=1, args=(average_total, average_score))
   
    # 新游戏 ranking by score
    df_ranking_by_score = df_score_total_0.sort_values(by=['average_comment'], ascending=False).reset_index()

    # 评分榜 写入 s_lcs_game_ranking_by_score
    db.write_to_mysql(df_ranking_by_score, db='game_process', tb="s_lcs_game_ranking_by_score_python", type='replace', index=True)  

def by_compre(df):
    # 综合榜
    df_compre = df.drop_duplicates(['game_format_name'])
    
    # nan , 得到天数
    df_compre = df_compre.fillna(0)
    df_compre['comment_time'] = df_compre['comment_time'].astype('int32')
    df_compre = df_compre[~(df_compre['comment_time'] == 0)]
    df_compre['days_diff_today'] = df_compre['comment_time'].apply(pre_treat.get_mistiming)
   
    # 评论数 fillna total=0 是nan
    df_compre = df_compre[df_compre['sum_total'] > 0]
    
    # 评分 format format_score  taptap 十分制
    df_compre['format_score'] = df_compre.apply(pre_treat.format_score, axis=1)
    
    # 计算
    df_compre['compre_heat'] = df_compre.apply(algorithm.get_compre, axis=1)
    
    # 新游戏 ranking by compre
    df_ranking_by_compre = df_compre.sort_values(by=['compre_heat'], ascending=False).reset_index()
    
    # 综合热度评分榜 写入 s_lcs_game_ranking_by_compre
    db.write_to_mysql(df_ranking_by_compre, db='game_process', tb="s_lcs_game_ranking_by_compre_python", type='replace', index=True)  
