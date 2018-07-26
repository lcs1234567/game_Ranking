import pymysql
import pandas as pd

# 获取数据
def get_df (sql, db):
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='eXYhzAWjyvy8grwM',db=db,charset='utf8mb4')
    df_game_download = pd.read_sql(sql, conn)  # 返回的是 dataFrame 数据结构
    conn.close()
    return df_game_download

# 写入 mysql
def write_to_mysql(df, db, tb, type='replace', index=False):  # type = replace 或 append
    from sqlalchemy import create_engine
    engine = create_engine("mysql+pymysql://root:eXYhzAWjyvy8grwM@127.0.0.1:3306/"+ db +"?charset=utf8mb4")
    df[['source','game_name','game_logo_url','score','tags']].to_sql(tb, 
        con=engine, if_exists=type, index=index)