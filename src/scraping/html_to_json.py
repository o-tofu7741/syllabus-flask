import glob
import json
from os import path

from bs4 import BeautifulSoup

# from pprint import pprint


current_dir = path.dirname(__file__)


def main():
    subjects = {}
    for p in glob.glob("C:/github/benten-scraping/GAKUEN/subjects/*.html"):
        # print(p)
        subjects[int(path.basename(p).rstrip(".html").replace("-", ""))] = get_subj(p)

    with open(path.join(path.dirname(__file__), "subjects_all2.json"), "w", encoding="utf-8") as f:
        json.dump(subjects, f, indent=2, ensure_ascii=False)


def get_subj(file_path):
    soup = BeautifulSoup(open(file_path, encoding="utf-8"), features="lxml")
    # print(soup.prettify())
    headers = soup.find_all(class_="ui-widget-header")
    contents = soup.find_all(class_="ui-widget-content")

    # 不要部分削除
    headers[19:23] = contents[23:25] = []  # カリキュラムマップ、ナンバリング
    headers[10:16] = contents[10:20] = []  # 授業時間外の連絡方法

    # for i in headers:
    #     print(list(i.stripped_strings))
    # for i in contents:
    #     print(list(i.stripped_strings))

    subj = {}

    # 開講年度-到達目標
    for h, c in zip(
        map(lambda x: list(x.stripped_strings)[0], headers[:13]),
        map(lambda x: list(x.stripped_strings), contents[:13]),
    ):
        if h in ["担当教員", "キーワード"]:
            subj[h] = " ".join(c).replace("　", "")
        else:
            subj[h] = r"\n".join(c).replace("　", "")
    headers[:13] = contents[:13] = []

    # アクティブ・ラーニング-実務教員科目
    for h, c1, c2 in zip(
        map(lambda x: list(x.stripped_strings)[0], headers[-6:-4]),
        map(lambda x: list(x.stripped_strings), contents[-8:-4:2]),
        map(lambda x: list(x.stripped_strings), contents[-7:-4:2]),
    ):
        subj[h] = [
            r"\n".join(c1).replace("　", ""),
            r"\n".join(c2).replace("　", ""),
        ]
    headers[-6:-4] = contents[-8:-4] = []

    # 学期末-履修上の注意
    for h, c in zip(
        map(lambda x: list(x.stripped_strings)[0], headers[-5:]),
        map(lambda x: list(x.stripped_strings), contents[-5:]),
    ):
        subj[h] = r"\n".join(c).replace("　", "")
    headers[-5:] = contents[-5:] = []

    # 授業回
    tmp = []
    for h, c1, c2 in zip(
        map(lambda x: list(x.stripped_strings)[0], headers),
        map(lambda x: list(x.stripped_strings), contents[0::2]),
        map(lambda x: list(x.stripped_strings), contents[1::2]),
    ):
        tmp.append(
            {
                "授業回": int(h),
                "概要": r"\n".join(c1).replace("　", ""),
                "事前事後学修内容": r"\n".join(c2).replace("　", ""),
            }
        )
    subj["授業計画"] = tmp

    return subj


if __name__ == "__main__":
    main()
