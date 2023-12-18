from glob import glob
from os import environ, path

import pymysql
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

app = Flask(__name__)

# MySQL接続設定
mysql_host = environ.get("DB_HOST", "")
mysql_port = int(environ.get("DB_PORT", 3306))
mysql_user = environ.get("MYSQL_APP_USER", "")
mysql_password = environ.get("MYSQL_APP_PASSWORD", "")
mysql_db = "subjects"
mysql_charset = "utf8mb4"

# MySQL接続確立
conn = pymysql.connect(
    host=mysql_host,
    port=mysql_port,
    user=mysql_user,
    password=mysql_password,
    db=mysql_db,
    charset=mysql_charset,
    cursorclass=pymysql.cursors.DictCursor,
)

id_list = tuple(
    map(
        lambda x: path.splitext(path.basename(x))[0],
        glob(path.join(path.dirname(__file__), "templates", "id", "*")),
    )
)


# フォームの送信を処理し、データベースをクエリする関数
def query_database(param):
    result = []
    try:
        with conn.cursor() as cursor:
            # print(param)
            sql = ["SELECT DISTINCT b.* FROM base b JOIN kai k ON b.id = k.id where 1=1"]
            sql_match = []
            where1 = []
            where2 = []
            v_args1 = []
            v_args2 = []
            v_args3 = []
            for k, v in param.items():
                if k in ("gakki", "gakunen", "yobi", "jigen"):
                    if len(v) == 1 and v[0] in ("", " "):
                        continue
                    where1.append(" ".join(["b." + k, "in", "(", ",".join(["%s"] * len(v)), ")"]))
                    v_args1 += list(map(int, v))
                else:
                    if len(v) == 1 and v[0] in ("", " "):
                        continue
                    if k in ("name", "teacher"):
                        where2.append(" ".join(["b." + k, "like", "%s"]))
                        v_args2.append("".join(["%", v[0], "%"]))
                    else:
                        continue
                        if v[0] not in ("", " "):
                            sql_match = [
                                "MATCH(b.name, b.teacher, b.keyword, b.gaiyo, b.mokuhyo, b.ActiveLearn, b.Jitsumu, b.seiseki_kijun, b.hyouka_ho, b.youi, b.risyu_chui,k.keikaku, k.naiyo) AGAINST (%s IN NATURAL LANGUAGE MODE)"
                            ]
                            v_args3.append(v[0])
            # if len(where2) == 0:
            #     where2.append("1=1 )")
            # else:
            #     where2[-1] = where2[-1] + "1=1 )"

            sql = " AND ".join(sql + where1 + where2 + sql_match) + ";"
            print(sql)
            print(v_args1 + v_args2 + v_args3)
            cursor.execute(sql, tuple(v_args1 + v_args2 + v_args3))
            result = cursor.fetchall()
    except Exception as e:
        print(f"Error querying database: {e}")
    finally:
        return result


@app.route("/")
@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        # フォームの送信を処理し、データベースをクエリします
        # subject_name = request.form["subject-name"][0]
        param = dict(request.form.lists())

        # データベースクエリを実行
        subjects = query_database(param)
        hoge = []
        for i in subjects:
            tmp = {}
            for k, v in i.items():
                if k == "gakki":
                    tmp[k] = "前期" if v == 1 else "後期" if v == 2 else "通年"
                elif k == "yobi":
                    tmp[k] = ("", "月", "火", "水", "木", "金", "土")[v]
                elif k == "id":
                    tmp["id_url"] = "id/" + str(v) + ".html"
                else:
                    tmp[k] = v
            hoge.append(tmp)

        # print(subjects[0])

        return render_template("search.html", subjects=hoge)

    return render_template("index.html")


@app.route("/id/<int:post_id>")
@app.route("/id/<int:post_id>.html")
def id(post_id):
    post_id = str(post_id)
    if post_id in id_list:
        return render_template("id/" + post_id + ".html")
    else:
        return "404 Not Found", 404


@app.errorhandler(404)
def page_not_found(error):
    return "404 Not Found", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
