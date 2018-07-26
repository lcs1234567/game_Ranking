from feature import get_feature
from rankingType import ranking_by
# 把各个指标 merge 到一个 df
def merge_features_to_df():
    # 下载指标
    df_detail = get_feature.f_downlaod()

    # 评论指标
    df_sum_total = get_feature.f_comments()

    # df_detail merge df_sum_total, 下载指标 评论数指标
    df_detail = df_detail.merge(df_sum_total, how='left', on='game_format_name')
    # nan = 0
    df_detail = df_detail.fillna(0)
    
    # time指标
    df_mix_time = get_feature.f_time()

    # df_detail 含 download_sum_num  sum_total  time
    df_detail_download_total_time = df_detail.merge(df_mix_time, how='left', on='game_format_name')

    # 去掉 vivo_game 因为没有tags
    df_dropVivo_detail_download_total_time = df_detail_download_total_time[~(df_detail_download_total_time['source'] == 'vivo_game')]
    return df_dropVivo_detail_download_total_time


if __name__ == '__main__':
    # merge download comments time 指标到一个df
    df_download_comments_time = merge_features_to_df()

    # 下载榜
    ranking_by.by_download(df_download_comments_time)
    
    # 热门榜
    ranking_by.by_comments(df_download_comments_time)
   
    # 新游榜
    ranking_by.by_time(df_download_comments_time)
    
    # 好评帮
    ranking_by.by_score(df_download_comments_time)
    
    # 综合热度榜
    ranking_by.by_compre(df_download_comments_time)
    
   







