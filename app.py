from flask import Flask, render_template_string, request, redirect, send_file
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

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

TEMPLATE="""
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial;margin:0;background:#f1f5f9;}
.sidebar{width:200px;height:100vh;background:#1e293b;color:white;position:fixed;}
.sidebar a{display:block;padding:12px;color:white;text-decoration:none;}
.sidebar a:hover{background:#334155;}
.top{margin-left:200px;background:#0ea5e9;color:white;padding:15px;}
.content{margin-left:200px;padding:20px;}

input,select,button{
width:100%;
padding:12px;
margin:8px 0;
font-size:16px;
}

.card{background:white;padding:15px;margin:10px;border-radius:10px;}

table{
width:100%;
border-collapse:collapse;
}
td,th{
border:1px solid #ccc;
padding:8px;
}

@media(max-width:768px){
.sidebar{width:100%;height:auto;position:relative;}
.top,.content{margin-left:0;}
}
</style>
</head>

<body>

<div class="sidebar">
<h3 style="padding:10px">MAY</h3>
<a href="/yonetici">Yönetici</a>
<a href="/veri">Veri Girişi</a>
<a href="/rapor">Rapor</a>
</div>

<div class="top">MAY SİSTEMİ</div>
<div class="content">{{content|safe}}</div>

</body>
</html>
"""

@app.route("/")
def home():
    return redirect("/yonetici")

# YÖNETİCİ
@app.route("/yonetici",methods=["GET","POST"])
def yonetici():

    if request.method=="POST":
        tip=request.form.get("tip")
        val=request.form.get("val")
        sil=request.form.get("sil")

        if val:
            if tip=="kisi":
                df=pd.read_excel(KISILER)
                df.loc[len(df)]=[val]
                df.to_excel(KISILER,index=False)

            if tip=="model":
                df=pd.read_excel(MODEL)
                df.loc[len(df)]=[val]
                df.to_excel(MODEL,index=False)

            if tip=="bant":
                df=pd.read_excel(BANT)
                df.loc[len(df)]=[val]
                df.to_excel(BANT,index=False)

            if tip=="operasyon":
                sure=request.form.get("sure")
                if sure:
                    df=pd.read_excel(OPERASYON)
                    df.loc[len(df)]=[val,int(sure)]
                    df.to_excel(OPERASYON,index=False)

        if sil:
            if tip=="kisi":
                df=pd.read_excel(KISILER)
                df=df[df["AdSoyad"]!=sil]
                df.to_excel(KISILER,index=False)

            if tip=="model":
                df=pd.read_excel(MODEL)
                df=df[df["Model"]!=sil]
                df.to_excel(MODEL,index=False)

            if tip=="bant":
                df=pd.read_excel(BANT)
                df=df[df["Bant"]!=sil]
                df.to_excel(BANT,index=False)

            if tip=="operasyon":
                df=pd.read_excel(OPERASYON)
                df=df[df["Operasyon"]!=sil]
                df.to_excel(OPERASYON,index=False)

    kisi=pd.read_excel(KISILER)
    model=pd.read_excel(MODEL)
    bant=pd.read_excel(BANT)
    op=pd.read_excel(OPERASYON)

    def tablo(df,tip,kolon):
        rows=""
        for i in df[kolon]:
            rows+=f"""
            <tr>
            <td>{i}</td>
            <td>
            <form method="post">
            <input type="hidden" name="sil" value="{i}">
            <button name="tip" value="{tip}">Sil</button>
            </form>
            </td>
            </tr>
            """
        return rows

    content=f"""
    <h3>Yönetici</h3>

    <div class="card">
    <h4>Kişiler</h4>
    <form method="post">
    <input name="val"><button name="tip" value="kisi">Ekle</button>
    </form>
    <table>{tablo(kisi,"kisi","AdSoyad")}</table>
    </div>

    <div class="card">
    <h4>Modeller</h4>
    <form method="post">
    <input name="val"><button name="tip" value="model">Ekle</button>
    </form>
    <table>{tablo(model,"model","Model")}</table>
    </div>

    <div class="card">
    <h4>Bant</h4>
    <form method="post">
    <input name="val"><button name="tip" value="bant">Ekle</button>
    </form>
    <table>{tablo(bant,"bant","Bant")}</table>
    </div>

    <div class="card">
    <h4>Operasyon</h4>
    <form method="post">
    <input name="val"><input name="sure">
    <button name="tip" value="operasyon">Ekle</button>
    </form>
    <table>{tablo(op,"operasyon","Operasyon")}</table>
    </div>
    """

    return render_template_string(TEMPLATE,content=content)

# VERİ
@app.route("/veri",methods=["GET","POST"])
def veri():
    kisiler=pd.read_excel(KISILER)
    ops=pd.read_excel(OPERASYON)
    bant=pd.read_excel(BANT)
    model=pd.read_excel(MODEL)

    if request.method=="POST":
        kisi=request.form.get("kisi")
        operasyon=request.form.get("operasyon")
        bantv=request.form.get("bant")
        modelv=request.form.get("model")
        saat=request.form.get("saat")
        adet=request.form.get("adet")

        if kisi and operasyon and bantv and modelv and saat and adet:
            try:
                sure=int(ops[ops["Operasyon"]==operasyon]["Sure"].values[0])
            except:
                sure=0

            df=pd.read_excel(DATA)
            df.loc[len(df)]=[
                datetime.now().strftime("%Y-%m-%d"),
                saat,kisi,operasyon,bantv,modelv,int(adet),sure
            ]
            df.to_excel(DATA,index=False)

    saatler=[f"{i}:00" for i in range(8,19)]

    content=f"""
    <h3>Veri Girişi</h3>

    <form method="post">
    <select name="kisi" required><option>Kişi</option>{''.join([f"<option>{i}</option>" for i in kisiler["AdSoyad"]])}</select>
    <select name="operasyon" required><option>Operasyon</option>{''.join([f"<option>{i}</option>" for i in ops["Operasyon"]])}</select>
    <select name="bant" required><option>Bant</option>{''.join([f"<option>{i}</option>" for i in bant["Bant"]])}</select>
    <select name="model" required><option>Model</option>{''.join([f"<option>{i}</option>" for i in model["Model"]])}</select>
    <select name="saat" required><option>Saat</option>{''.join([f"<option>{i}</option>" for i in saatler])}</select>
    <input name="adet" type="number" placeholder="Adet" required>
    <button>Kaydet</button>
    </form>
    """

    return render_template_string(TEMPLATE,content=content)

# RAPOR
@app.route("/rapor")
def rapor():
    df=pd.read_excel(DATA)

    dosya="rapor.xlsx"
    df.to_excel(dosya,index=False)

    content=f"""
    <h3>Rapor</h3>
    {df.to_html(index=False)}
    <br><br>
    <a href="/indir">Excel indir</a>
    """

    return render_template_string(TEMPLATE,content=content)

@app.route("/indir")
def indir():
    return send_file("rapor.xlsx",as_attachment=True)

if __name__=="__main__":
    app.run()
