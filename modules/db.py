"""データベースの操作をまとめる"""

import pandas as pd
import sqlite3


DB_NAME = "datas/test.db"
TABLE_NAME = "company_information"
CSV_NAME = "datas/test.csv"
JSON_NAME = "datas/test.json"


class DataBase:
    """データベースの操作する

    Attributes:
        con: 接続したデータベース
        cursor: データベースを操作するカーソル

    Notes:
        最後には必ずconをcloseすること

    """
    def __init__(self, db_name: str):
        self.con = sqlite3.connect(database=db_name)
        self.cursor = self.con.cursor()

    def execute_query(self, *query):
        """クエリを実行して変更をコミックする

        Args:
            *query: クエリ文

        """
        self.cursor.execute(*query)
        self.con.commit()

    def change_from_db_to_df(self) -> pd.DataFrame:
        """データベースをデータフレームに読み込む

        Returns:
            df: データベースを読み込んだデータフレーム

        Notes:
            実行後、conをcloseする

        """
        ## データベースをデータフレームに読み込む
        read_query = f"SELECT * FROM {TABLE_NAME}"
        df = pd.read_sql_query(read_query, self.con)
        self.con.close()
        return df

    def change_from_df_csv(self, df: pd.DataFrame, csv_name: str):
        """データフレームをcsvに変換する"""
        df.to_csv(csv_name, index=False)

    def change_from_df_json(self, df: pd.DataFrame, json_name: str):
        """データフレームをjsonに変換する"""
        df.to_json(json_name, orient="records", lines=True)


def main():
    ## データベースに接続
    db = DataBase(db_name=DB_NAME)
    ## テーブルを作成する
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
        title TEXT,
        company_name TEXT,
        info_update_date DATE,
        posting_end_date DATE
    );
    """
    db.execute_query(create_table_query)
    ## テーブルを空にする
    db.execute_query(f"DELETE FROM {TABLE_NAME}")
    ## データベースを閉じる
    db.con.close()

    ## データベースからcsvとjsonを出力
    # db = DataBase(db_name=DB_NAME)
    # df = db.change_from_db_to_df()
    # db.change_from_df_csv(df=df, csv_name=CSV_NAME)
    # db.change_from_df_json(df=df, json_name=JSON_NAME)

if __name__ == "__main__":
    main()