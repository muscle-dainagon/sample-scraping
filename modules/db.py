"""データベースの操作をまとめる"""

import sqlite3


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


def main():
    ## データベースに接続
    db = DataBase(db_name="datas/test.db")
    ## テーブルを作成する
    create_table_query = """
    CREATE TABLE IF NOT EXISTS company_information(
        title TEXT,
        company_name TEXT,
        info_update_date DATE,
        posting_end_date DATE
    );
    """
    db.execute_query(create_table_query)
    ## テーブルを空にする
    db.execute_query("DELETE FROM company_information")
    ## データベースを閉じる
    db.con.close()

if __name__ == "__main__":
    main()