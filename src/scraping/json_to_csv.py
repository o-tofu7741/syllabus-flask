import csv
import json
from os import path

with open(path.join(path.dirname(__file__), "subjects_all2.json"), "r", encoding="utf-8") as f:
    subj: dict = json.load(f)

taio = {
    "開講年度": "id",
    "最終更新日時": "year",
    "科目名": "name",
    "科目区分": "kubun",
    "授業形態": "keitai",
    "単位数": "tani",
    "配当学年": "gakunen",
    "開講学期": "gakki",
    "時間割コード": "subj_id",
    "担当教員": "teacher",
    "キーワード": "keyword",
    "授業科目の概要": "gaiyo",
    "本授業の到達目標": "mokuhyo",
    # "アクティブ・ラーニング":"isActiveLearn","ActiveLearn",
    # "実務教員科目":
    "学期末試験": "kimatsu",
    "成績評価基準": "seiseki_kijun",
    "評価の方法・総合評価割合": "hyouka_hou",
    "テキスト等、学修のために購入・準備が必要なもの": "youi",
    "履修上の注意事項、事前・事後学修に必要な目安時間、フィードバックの方法、学修上の助言": "risyu_chui",
}

base = [
    [
        "id",
        "yobi",
        "jigen",
        "year",
        "name",
        "kubun",
        "keitai",
        "tani",
        "gakunen",
        "gakki",
        "subj_id",
        "teacher",
        "keyword",
        "gaiyo",
        "mokuhyo",
        "isActiveLearn",
        "ActiveLearn",
        "isJitsumu",
        "Jitsumu",
        "kimatsu",
        "seiseki_kijun",
        "hyouka_ho",
        "youi",
        "risyu_chui",
    ]
]
kai = [["id", "n_kai", "keikaku", "naiyo"]]

for k, v in subj.items():
    ks = str(k)
    tmp = [ks, ks[0], ks[1]]
    for k2, v2 in v.items():
        if k2 not in ["最終更新日時", "授業計画"]:
            if k2 in ["アクティブ・ラーニング", "実務教員科目"]:
                tmp += v2
            else:
                if k2 == "単位数":
                    tmp.append(v2.replace("単位", ""))
                elif k2 == "開講年度":
                    tmp.append(v2.replace("年度", ""))
                elif k2 == "配当学年":
                    if v2 in ["1年", "2年", "3年", "4年"]:
                        tmp.append(v2.replace("年", ""))
                    else:
                        tmp.append("0")
                elif k2 == "開講学期":
                    if "前期" == v2:
                        tmp.append("1")
                    elif "後期" == v2:
                        tmp.append("2")
                    else:
                        tmp.append("0")
                else:
                    tmp.append(v2)
        elif k2 == "授業計画":
            for i in v2:
                kai.append(
                    [str(k)]
                    + list(map(lambda x: x if type(x) is int else x.replace('"', "''"), i.values()))
                )
    base.append(list(map(lambda x: x.replace('"', "''"), tmp)))
# print(base[:4])


# ['3単位', '5単位', '6単位', '8単位', '2単位', '1単位', '4単位']
# ['1年', 'カリキュラムにより異なります。', '2年', '3年', '4年', '学年指定なし']
# ['前期', '前期～後期', '後期']
# ["開講年度","科目名","科目区分","授業形態","単位数","配当学年","開講学期","時間割コード","担当教員","キーワード","授業科目の概要","本授業の到達目標","アクティブ・ラーニング",""]


with open(path.join(path.dirname(__file__), "base"), "w", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL, lineterminator="\t")
    writer.writerows(base)

with open(path.join(path.dirname(__file__), "kai"), "w", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL, lineterminator="\t")
    writer.writerows(kai)
