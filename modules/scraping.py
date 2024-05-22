"""マイナビ転職から求人情報をスクレイピング操作をまとめる"""

from bs4 import BeautifulSoup
import datetime
import requests
from time import sleep


def parse_html(url: str) -> BeautifulSoup:
    """HTMLの構造を解析する

    Args:
        url: 解析するURL

    Returns:
        soup: HTMLコンテンツ全体

    """
    res = requests.get(url=url)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


def get_company_links(soup: BeautifulSoup) -> list:
    """会社のリンクの情報を取得する

    Args:
        soup: HTMLコンテンツ全体

    Returns:
        links_data: 会社のリンクの情報を格納したリスト

    """
    ROOT_URL = "https:"
    links_data = []
    links = soup.find_all("a", attrs={"class", "js__ga--setCookieOccName"}) # 引数attrsでclassを指定する attrs={"class", "<クラス名>"}
    for link in links:
        href = link["href"]
        if href:
            url = ROOT_URL + href
            if url not in links_data:
                links_data.append(url)
    return links_data


def get_company_info(link: str):
    """リンクから「タイトル」「会社名」「情報更新日」「掲載終了予定日」を取得する

    Args:
        link: 会社のリンク

    Returns:
        title: タイトル
        company_name: 会社名
        info_update_date: 情報更新日
        posting_end_date: 掲載終了予定日

    """
    soup = parse_html(url=link)
    ## タイトル
    title = soup.find("span", attrs={"class", "occName"}).text
    ## 会社名
    company_name = soup.find("span", attrs={"class", "companyName"}).text
    ## 情報更新日と掲載終了予定日
    date_info = soup.find("div", attrs={"class", "dateInfo"}).text
    date_info = date_info.split("：")
    info_update_date = date_info[1].replace("掲載終了予定日", "")
    info_update_date = datetime.datetime.strptime(info_update_date, "%Y/%m/%d").date() # 日付型に変換
    posting_end_date = date_info[-1]
    return title, company_name, info_update_date, posting_end_date


def main():
    soup = parse_html(url="https://tenshoku.mynavi.jp/list/")
    links_data = get_company_links(soup=soup)
    ## 数を絞るために、データをスライス
    links_data = links_data[:3]
    links_data
    ## クロール
    for i ,link in enumerate(links_data):
        title, company_name, info_update_date, posting_end_date = get_company_info(link=link)
        print(title, company_name, info_update_date, posting_end_date)
        sleep(30)

if __name__ == "__main__":
    main()