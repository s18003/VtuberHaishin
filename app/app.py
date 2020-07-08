#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask, render_template, request, redirect, url_for
from models.models import VtuberContent, VtuberName
from models.database import db_session
#from datetime import datetime
import requests, bs4, re


#Flaskオブジェクトの生成
app = Flask(__name__)

#スクレイピング処理検証　確認後コメントアウトすること
res = requests.get('https://virtual-youtuber.userlocal.jp/schedules')
b_soup = bs4.BeautifulSoup(res.content, 'html.parser')


#「/」へアクセスがあった場合に、index.htmlを返す
@app.route("/")
@app.route("/index")
def index():
    name = request.args.get("name")
    all_name = VtuberName.query.all()
    all_vtuber = VtuberContent.query.all()
    return render_template("index.html",name=name,all_vtuber=all_vtuber,all_name=all_name)



#formから/addにpostあった時
@app.route("/add", methods=["post"])
def add():
    dareyanen = request.form["name"]
    vname = b_soup.find_all(class_="no-propagation", text=re.compile(".*" + dareyanen + ".*"))
    if vname == []:
        naiyo = "配信予定が現在無いか、存在しないVtuberです"
        all_name = VtuberName.query.all()
        all_vtuber = VtuberContent.query.all()
        return render_template("index.html", naiyo=naiyo,all_vtuber=all_vtuber,all_name=all_name)
    else:
        haishinsya = vname[0].text
        haishinurl = vname[0].get('href')
        content = VtuberName(haishinsya, haishinurl)
        db_session.add(content)
        db_session.commit()
        oya = vname[0].find_parents("span")
        haisihinmei = oya[0].find_previous_siblings("a")
        tdtagu = oya[0].find_parents("td")  # まずspanの親要素のtdとってくる
        trtagu = tdtagu[0].find_parents("tr")  # 更にさっきとってきたtdの親要素であるtrとってくる
        hinititr = trtagu[0].find_previous_sibling(class_="row-header")  # trと兄弟要素の何日かあるtrタグとってくる
        hourtagu = trtagu[0].find("div")  # trの下にある時間が記載されているdivをとってくる
        if hourtagu:
            False
        else:
            oyazikan = trtagu[0].find_previous_sibling(class_="row-content row-content-hour-changed"),
            hourgaarutagu = oyazikan[0].find_all(class_="hour")
        haishin1 = haisihinmei[0].text  # 配信タイトル
        haishin2 = vname[0].text  # 配信者名
        #haishin3 = hinititr.text.strip()   #配信日
        #以下条件分岐は配信時間
        if hourtagu:
            zikan = hinititr.text.strip() + hourtagu.text
        else:
            zikan = hinititr.text.strip() + hourgaarutagu[0].text
        haishin6 = vname[0].get('href')  # 配信者情報URL
        haishin7 = haisihinmei[0].get('href')  # 配信URL
        content = VtuberContent(haishin1, haishin2, zikan, haishin6, haishin7)
        db_session.add(content)
        db_session.commit()
        return index()

"""
for kurikaesi in dareyanen:
        vname = b_soup.find_all(class_="no-propagation", text=re.compile(".*" + kurikaesi.name + ".*"))
        if vname == []:
            continue
        else:
            oya = vname[0].find_parents("span")
            haisihinmei = oya[0].find_previous_siblings("a")
            tdtagu = oya[0].find_parents("td")      #まずspanの親要素のtdとってくる
            trtagu = tdtagu[0].find_parents("tr")   #更にさっきとってきたtdの親要素であるtrとってくる
            hinititr = trtagu[0].find_previous_sibling(class_="row-header") #trと兄弟要素の何日かあるtrタグとってくる
            hourtagu = trtagu[0].find("div")        #trの下にある時間が記載されているdivをとってくる
            if hourtagu:
                False
            else:
                oyazikan = trtagu[0].find_previous_sibling(class_="row-content row-content-hour-changed"),
                hourgaarutagu = oyazikan[0].find_all(class_="hour")
            haishin1 = haisihinmei[0].text     #配信タイトル
            haishin2 = vname[0].text           #配信者名
            #haishin3 = hinititr.text.strip()   #配信日
            #以下条件分岐は配信時間
            if hourtagu:
                zikan = hinititr.text.strip() + hourtagu.text
            else:
                zikan = hinititr.text.strip() + hourgaarutagu[0].text
            haishin6 = vname[0].get('href')       #配信者情報URL
            haishin7 = haisihinmei[0].get('href') #配信URL
            content = VtuberContent(haishin1, haishin2, zikan, haishin6, haishin7)
            db_session.add(content)
            db_session.commit()
#ここまで
"""

"""
#「/」へアクセスがあった場合に、index.htmlを返す
@app.route("/")
@app.route("/index")
def index():
    name = request.args.get("name")
    all_vtuber = VtuberContent.query.all()
    #okyo = [haishin1, haishin2, zikan()]
    #haiURL = [haishin6, haishin7] #7が配信待機 or 配信中なら直接ようつべに飛ぶ、なければ配信者URLに飛ぶらしい
    return render_template("index.html",name=name,all_vtuber=all_vtuber)
"""

#/indexにpost送られてきた時の処理
@app.route("/index",methods=["post"])
def post():
    name = request.form["name"]
    #okyo = ["色不異空", "空不異色", "色即是空", "空即是色"]
    all_vtuber = VtuberContent.query.all()
    return render_template("index.html", name=name, all_vtuber=all_vtuber)


#名前のみの方の削除処理
@app.route("/delete",methods=["post"])
def delete():
    id_list = request.form.getlist("delete")
    for id in id_list:
        content = VtuberName.query.filter_by(id=id).first()
        db_session.delete(content)
    db_session.commit()
    return index()

#放送タイトルとか全部の選択式削除処理
@app.route("/kesu",methods=["post"])
def kesu():
    id_list = request.form.getlist("kesu")
    for id in id_list:
        content = VtuberContent.query.filter_by(id=id).first()
        db_session.delete(content)
    db_session.commit()
    return index()

#更新処理
@app.route("/update",methods=["post"])
def update():
    db_session.query(VtuberContent).delete()
    db_session.commit()
    dareyanen = VtuberName.query.all()
    res = requests.get('https://virtual-youtuber.userlocal.jp/schedules')
    b_soup = bs4.BeautifulSoup(res.content, 'html.parser')
    for kurikaesi in dareyanen:
        vname = b_soup.find_all(class_="no-propagation", text=re.compile(".*" + kurikaesi.name + ".*"))
        if vname == []:
            continue
        else:
            oya = vname[0].find_parents("span")
            haisihinmei = oya[0].find_previous_siblings("a")
            tdtagu = oya[0].find_parents("td")      #まずspanの親要素のtdとってくる
            trtagu = tdtagu[0].find_parents("tr")   #更にさっきとってきたtdの親要素であるtrとってくる
            hinititr = trtagu[0].find_previous_sibling(class_="row-header") #trと兄弟要素の何日かあるtrタグとってくる
            hourtagu = trtagu[0].find("div")        #trの下にある時間が記載されているdivをとってくる
            if hourtagu:
                False
            else:
                oyazikan = trtagu[0].find_previous_sibling(class_="row-content row-content-hour-changed"),
                hourgaarutagu = oyazikan[0].find_all(class_="hour")
            haishin1 = haisihinmei[0].text     #配信タイトル
            haishin2 = vname[0].text           #配信者名
            #haishin3 = hinititr.text.strip()   #配信日
            #以下条件分岐は配信時間
            if hourtagu:
                zikan = hinititr.text.strip() + hourtagu.text
            else:
                zikan = hinititr.text.strip() + hourgaarutagu[0].text
            haishin6 = vname[0].get('href')       #配信者情報URL
            haishin7 = haisihinmei[0].get('href') #配信URL
            content = VtuberContent(haishin1, haishin2, zikan, haishin6, haishin7)
            db_session.add(content)
            db_session.commit()
    return index()


"""
#formから/addで送られてきた時の処理
@app.route("/add",methods=["post"])
def add():
    title = request.form["title"]
    name = request.form["name"]
    date = request.form["date"]
    url1 = request.form["url1"]
    url2 = request.form["url2"]
    #以下DBに追加する処理
    content = VtuberContent(title, name, date, url1, url2)
    db_session.add(content)
    db_session.commit()
    return index()
"""

"""
～やること～
table定義で新しくVtuberNamaeを作成 参考サイトが２つ目のテーブル作成時でヨシ
列定義はid = Column(Integer, primary_key=True) と vnamae = Column(String(100))
そんでもって作ったら、/addで受け取るやつをスクレイピング処理より上に持ってくる
でなんやかんやで書くとこにテーブルに格納してる配信者名をスクレイピングにかけて書くとこにブチこむ　がんばれ

"""

if __name__ == "__main__":
    app.run(debug=True)
