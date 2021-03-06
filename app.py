"""Làm một website tuyển dụng.
Lấy dữ liệu các job từ: https://github.com/awesome-jobs/vietnam/issues
Lưu dữ liệu vào một bảng jobs trong SQLite. 
Tạo website hiển thị danh sách các jobs khi vào đường dẫn /.
Khi bấm vào mỗi job (1 link), sẽ mở ra trang chi tiết về jobs (giống như trên
các trang web tìm viêc)."""

import requests
import json
import sqlite3
from flask import Flask
from flask import render_template
from flask import jsonify

app = Flask(__name__)


def create():
    """Tạo file db thêm dữ liệu lấy từ https://github.com/awesome-jobs/vietnam/issues cho vào bảng jobs"""
    conn = sqlite3.connect("jobspython.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE jobs(number int, name text, url text)""")
    conn.commit()
    for i in range(1, 11):
        r = requests.get(
            "https://api.github.com/repos/awesome-jobs/vietnam/issues?page={}".format(i)
        )
        data = json.loads(r.text)
        if data == []:
            break
        for job in data:
            conn = sqlite3.connect("jobspython.db")
            c = conn.cursor()
            a = """INSERT INTO jobs VALUES ({}, '{}', '{}');""".format(
                job["number"], job["title"], job["html_url"]
            )
            c.execute(a)
            conn.commit()
        data = []


@app.route("/")
def web():
    result = []
    create()
    conn = sqlite3.connect("jobspython.db")
    c = conn.cursor()
    c.execute("SELECT * FROM jobs")
    ans = c.fetchall()
    for id, title, link in ans:
        job = "{}: {}\n".format(id, title)
        result.append([job, link])
    c.execute("DROP TABLE jobs")
    return render_template("index.html", content=result)


if __name__ == "__main__":
    app.run(debug=True)
