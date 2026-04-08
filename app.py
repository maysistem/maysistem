from flask import Flask, render_template_string, request, redirect, send_file
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

pd.options.mode.chained_assignment = None

KISILER="kisiler.xlsx"
OPERASYON="operasyon.xlsx"
MODEL="model.xlsx"
BANT="bant.xlsx"
DATA="data.xlsx"

def init():
    if not os.path.exists(KISILER):
        pd.DataFrame(columns=["AdSoyad"]).to_excel(KISILER,index=False)
    if not os.path.exists(OPERASYON):
        pd.DataFrame(columns=["Operasyon","Sure"]).to_excel(OPERASYON,index=False)
    if not os.path.exists(MODEL):
        pd.DataFrame(columns=["Model"]).to_excel(MODEL,index=False)
    if not os.path.exists(BANT):
        pd.DataFrame(columns=["Bant"]).to_excel(BANT,index=False)
    if not os.path.exists(DATA):
        pd.DataFrame(columns=["Tarih","Saat","AdSoyad","Operasyon","Bant","Model","Adet","Sure"]).to_excel(DATA,index=False)

init()

TEMPLATE = """
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {font-family:Arial; margin:0; background:#f1f5f9;}
.sidebar {width:220px;height:100vh;background:#1e293b;color:white;position:fixed;}
.sidebar h2 {padding:20px;}
.sidebar a {display:block;padding:12px;color:white;text-decoration:none;}
.sidebar a:hover {background:#334155;}
.top {margin-left:220px;background:#0ea5e9;color:white;padding:15px;}
.content {margin-left:220px;padding:20px;}
.card {background:white;padding:15px;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.1);}
@media (max-width:768px){
.sidebar{width:100%;height:auto;position:relative;}
.top{margin-left:0;text-align:center;}
.content{margin-left:0;}
input,button,select{width:100%;padding:10px;margin:5px 0;}
table{display:block;overflow-x:auto;font-size:12px;}
}
</style>
</head>
<body>

<div class="sidebar">
<h2>MAY</h2>
<a href="/yonetici">Yönetici</a>
<a href="/veri">Üretim Veri Girişi</a>
<a href="/rapor">Raporlar</a>
</div>

<div class="top"><h2>MAY SİSTEMİ</h2></div>

<div class="content">
{{content|safe}}
</div>

</body>
</html>
"""

@app.route("/")
def home():
    return redirect("/yonetici")

@app.route("/yonetici", methods=["GET","POST"])
def yonetici():
    if request.method=="POST":
        tip=request.form.get("tip")
        val=request.form.get("val")

        if val:
            if tip=="kisi":
                df=pd.read_excel(KISILER); df.loc[len(df)]=[val]; df.to_excel(KISILER,index=False)
            if tip=="model":
                df=pd.read_excel(MODEL); df.loc[len(df)]=[val]; df.to_excel(MODEL,index=False)
            if tip=="bant":
                df=pd.read_excel(BANT); df.loc[len(df)]=[val]; df.to_excel(BANT,index=False)
            if tip=="operasyon":
                sure=request.form.get("sure")
                if sure:
                    df=pd.read_excel(OPERASYON); df.loc[len(df)]=[val,int(sure)]; df.to_excel(OPERASYON,index=False)

    content="<h3>Yönetici Paneli aktif</h3>"
    return render_template_string(TEMPLATE,content=content)

@app.route("/veri")
def veri():
    return render_template_string(TEMPLATE,content="<h3>Veri sayfası</h3>")

@app.route("/rapor")
def rapor():
    return render_template_string(TEMPLATE,content="<h3>Rapor sayfası</h3>")

@app.route("/indir")
def indir():
    return send_file("rapor.xlsx",as_attachment=True)

if __name__=="__main__":
    app.run()
