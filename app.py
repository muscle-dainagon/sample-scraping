"""マイナビ転職から求人情報をスクレイピング"""
import datetime
import math
from time import sleep

from modules.db import DataBase, DB_NAME, TABLE_NAME, CSV_NAME, JSON_NAME
from modules.scraping import parse_html, get_company_links, get_company_info


## 会社のリンクの情報を取得する
soup = parse_html(url="https://tenshoku.mynavi.jp/list/")
links_data = get_company_links(soup=soup)
## 開始時間
start_time = datetime.datetime.now()
## クロール
for i ,link in enumerate(links_data):
    title, company_name, info_update_date, posting_end_date = get_company_info(link=link)
    ## データベースに挿入する
    db = DataBase(db_name=DB_NAME)
    insert_query = f"""
    INSERT INTO {TABLE_NAME} (title, company_name, info_update_date, posting_end_date)
    VALUES(?, ?, ?, ?);
    """
    data = (title, company_name, info_update_date, posting_end_date)
    db.execute_query(insert_query, data)
    db.con.close()
    ## 状況表示
    print(f"{i+1}件目終了")
    ## ディレイ
    sleep(30)
## 終了時間
end_time = datetime.datetime.now()
## 実行時間
time_difference = end_time - start_time
time_difference = time_difference.total_seconds() / 3600 ## 秒→時に変換
## 時間経過表示
print("開始時間: " + start_time.strftime("%Y/%m/%d %H:%M:%S"))
print("終了時間: " + end_time.strftime("%Y/%m/%d %H:%M:%S"))
print("実行時間: " + str(math.ceil(time_difference * 100) / 100) + "時間") ## 小数第2位を切り上げ
## データベースからcsvとjsonに出力
db = DataBase(db_name=DB_NAME)
df = db.change_from_db_to_df()
db.change_from_df_csv(df=df, csv_name=CSV_NAME)
db.change_from_df_json(df=df, json_name=JSON_NAME)