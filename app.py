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

TEMPLATE = """
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {font-family:Arial; margin:0; background:#f1f5f9;}

.sidebar {
    width:220px;
    height:100vh;
    background:#1e293b;
    color:white;
    position:fixed;
}

.sidebar h2 {padding:20px;}

.sidebar a {
    display:block;
    padding:12px;
    color:white;
    text-decoration:none;
}

.sidebar a:hover {background:#334155;}

.top {
    margin-left:220px;
    background:#0ea5e9;
    color:white;
    padding:15px;
}

.content {
    margin-left:220px;
    padding:20px;
}

.card {
    background:white;
    padding:15px;
    border-radius:10px;
    box-shadow:0 2px 8px rgba(0,0,0,0.1);
    min-width:250px;
}

/* MOBİL */
@media (max-width:768px){
    .sidebar{width:100%; height:auto; position:relative;}
    .top{margin-left:0; text-align:center;}
    .content{margin-left:0;}
    input,button,select{width:100%; padding:10px; margin:5px 0;}
    table{display:block; overflow-x:auto; font-size:12px;}
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

<div class="top">
<h2>MAY SİSTEMİ</h2>
</div>

<div class="content">
{{content|safe}}
</div>

</body>
</html>
"""

@app.route("/")
def home():
    return redirect("/yonetici")

# YÖNETİCİ
@app.route("/yonetici", methods=["GET","POST"])
def yonetici():
    if request.method=="POST":
        tip=request.form["tip"]
        val=request.form["val"]

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
            sure=request.form["sure"]
            df=pd.read_excel(OPERASYON)
            df.loc[len(df)]=[val,int(sure)]
            df.to_excel(OPERASYON,index=False)

    kisi_df = pd.read_excel(KISILER)
    model_df = pd.read_excel(MODEL)
    bant_df = pd.read_excel(BANT)
    op_df = pd.read_excel(OPERASYON)

    content = f"""
    <h3>Yönetici Paneli</h3>

    <div style="display:flex; gap:20px; flex-wrap:wrap;">

    <div class="card">
    <h4>Kişiler</h4>
    <form method="post">
    <input name="val" placeholder="Ad Soyad">
    <button name="tip" value="kisi">Ekle</button>
    </form>
    {kisi_df.to_html(index=False)}
    </div>

    <div class="card">
    <h4>Modeller</h4>
    <form method="post">
    <input name="val" placeholder="Model">
    <button name="tip" value="model">Ekle</button>
    </form>
    {model_df.to_html(index=False)}
    </div>

    <div class="card">
    <h4>Bantlar</h4>
    <form method="post">
    <input name="val" placeholder="Bant">
    <button name="tip" value="bant">Ekle</button>
    </form>
    {bant_df.to_html(index=False)}
    </div>

    <div class="card">
    <h4>Operasyon</h4>
    <form method="post">
    <input name="val" placeholder="Operasyon">
    <input name="sure" placeholder="sn">
    <button name="tip" value="operasyon">Ekle</button>
    </form>
    {op_df.to_html(index=False)}
    </div>

    </div>
    """

    return render_template_string(TEMPLATE,content=content)

# VERİ GİRİŞ
@app.route("/veri", methods=["GET","POST"])
def veri():
    kisiler=pd.read_excel(KISILER)
    ops=pd.read_excel(OPERASYON)
    bant=pd.read_excel(BANT)
    model=pd.read_excel(MODEL)

    if request.method=="POST":
        kisi=request.form["kisi"]
        operasyon=request.form["operasyon"]
        bantv=request.form["bant"]
        modelv=request.form["model"]
        saat=request.form["saat"]
        adet=request.form["adet"]

        sure=int(ops[ops["Operasyon"]==operasyon]["Sure"].values[0])

        df=pd.read_excel(DATA)
        df.loc[len(df)]=[
            datetime.now().strftime("%Y-%m-%d"),
            saat,kisi,operasyon,bantv,modelv,int(adet),sure
        ]
        df.to_excel(DATA,index=False)

    data=pd.read_excel(DATA)
    saatler = [f"{s:02d}:00" for s in range(8,19)]

    content = f"""
    <h3>Üretim Veri Girişi</h3>

    <form method="post">

    Kişi:
    <select name="kisi" required>
    <option value="">Seç</option>
    {''.join([f"<option>{i}</option>" for i in kisiler["AdSoyad"]])}
    </select><br>

    Operasyon:
    <select name="operasyon" required>
    <option value="">Seç</option>
    {''.join([f"<option>{i}</option>" for i in ops["Operasyon"]])}
    </select><br>

    Bant:
    <select name="bant" required>
    <option value="">Seç</option>
    {''.join([f"<option>{i}</option>" for i in bant["Bant"]])}
    </select><br>

    Model:
    <select name="model" required>
    <option value="">Seç</option>
    {''.join([f"<option>{i}</option>" for i in model["Model"]])}
    </select><br>

    Saat:
    <select name="saat" required>
    <option value="">Seç</option>
    {''.join([f"<option>{s}</option>" for s in saatler])}
    </select><br>

    Adet:
    <input name="adet" type="number" required><br>

    <button>Kaydet</button>
    </form>

    <h3>Kayıtlar</h3>
    {data.to_html()}
    """

    return render_template_string(TEMPLATE,content=content)

# RAPOR
@app.route("/rapor")
def rapor():
    df=pd.read_excel(DATA)

    if len(df)>0:
        df["Performans %"]=(df["Adet"]*df["Sure"])/540*100

    dosya="rapor.xlsx"
    df.to_excel(dosya,index=False)

    content=f"""
    <h3>Raporlar</h3>
    {df.to_html()}
    <br><a href="/indir">Excel indir</a>
    """

    return render_template_string(TEMPLATE,content=content)

@app.route("/indir")
def indir():
    return send_file("rapor.xlsx",as_attachment=True)

if __name__=="__main__":
    app.run()from flask import Flask, render_template_string, request, redirect, send_file
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# Dosyalar
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
<style>
body {font-family:Arial; margin:0;}
.sidebar {width:220px; height:100vh; background:#1e293b; color:white; float:left;}
.sidebar h2 {padding:20px;}
.sidebar a {display:block; padding:12px; color:white; text-decoration:none;}
.sidebar a:hover {background:#334155;}
.top {margin-left:220px; background:#0ea5e9; color:white; padding:15px;}
.content {margin-left:220px; padding:20px;}
.card {background:#f1f5f9; padding:10px; margin:10px 0;}
</style>
</head>

<body>

<div class="sidebar">
<h2>MAY</h2>
<a href="/yonetici">Yönetici</a>
<a href="/veri">Üretim Veri Girişi</a>
<a>Kumaş Kontrol</a>
<a>Aksesuar Kontrol</a>
<a>Sipariş Listesi</a>
<a href="/rapor">Raporlar</a>
</div>

<div class="top">
<h2>MAY SİSTEMİ</h2>
</div>

<div class="content">
{{content|safe}}
</div>

</body>
</html>
"""

@app.route("/")
def home():
    return redirect("/yonetici")

# YÖNETİCİ
@app.route("/yonetici", methods=["GET","POST"])
def yonetici():
    if request.method=="POST":
        tip=request.form["tip"]
        val=request.form["val"]
        if tip=="kisi":
            df=pd.read_excel(KISILER); df.loc[len(df)]=[val]; df.to_excel(KISILER,index=False)
        if tip=="model":
            df=pd.read_excel(MODEL); df.loc[len(df)]=[val]; df.to_excel(MODEL,index=False)
        if tip=="bant":
            df=pd.read_excel(BANT); df.loc[len(df)]=[val]; df.to_excel(BANT,index=False)
        if tip=="operasyon":
            sure=request.form["sure"]
            df=pd.read_excel(OPERASYON); df.loc[len(df)]=[val,int(sure)]; df.to_excel(OPERASYON,index=False)

    content="""
    <h3>Yönetici Paneli</h3>

    <form method="post">
    <input name="val" placeholder="Ad Soyad">
    <button name="tip" value="kisi">Kişi Ekle</button>
    </form>

    <form method="post">
    <input name="val" placeholder="Model">
    <button name="tip" value="model">Model Ekle</button>
    </form>

    <form method="post">
    <input name="val" placeholder="Bant">
    <button name="tip" value="bant">Bant Ekle</button>
    </form>

    <form method="post">
    <input name="val" placeholder="Operasyon">
    <input name="sure" placeholder="sn">
    <button name="tip" value="operasyon">Operasyon Ekle</button>
    </form>
    """

    return render_template_string(TEMPLATE,content=content)

# VERİ GİRİŞ
@app.route("/veri", methods=["GET","POST"])
def veri():
    kisiler=pd.read_excel(KISILER)
    ops=pd.read_excel(OPERASYON)
    bant=pd.read_excel(BANT)
    model=pd.read_excel(MODEL)

    if request.method=="POST":
        kisi=request.form["kisi"]
        operasyon=request.form["operasyon"]
        bantv=request.form["bant"]
        modelv=request.form["model"]
        saat=request.form["saat"]
        adet=request.form["adet"]

        sure=int(ops[ops["Operasyon"]==operasyon]["Sure"].values[0])

        df=pd.read_excel(DATA)
        df.loc[len(df)]=[datetime.now().strftime("%Y-%m-%d"),saat,kisi,operasyon,bantv,modelv,int(adet),sure]
        df.to_excel(DATA,index=False)

    data=pd.read_excel(DATA)

    content=f"""
    <h3>Üretim Veri Girişi</h3>

    <form method="post">
    Kişi:<input name="kisi"><br>
    Operasyon:<input name="operasyon"><br>
    Bant:<input name="bant"><br>
    Model:<input name="model"><br>
    Saat:<input name="saat" placeholder="08:00-18:00"><br>
    Adet:<input name="adet"><br>
    <button>Kaydet</button>
    </form>

    <h3>Kayıtlar</h3>
    {data.to_html()}
    """

    return render_template_string(TEMPLATE,content=content)

# RAPOR
@app.route("/rapor")
def rapor():
    df=pd.read_excel(DATA)
    if len(df)>0:
        df["Performans %"]=(df["Adet"]*df["Sure"])/540*100

    dosya="rapor.xlsx"
    df.to_excel(dosya,index=False)

    content=f"""
    <h3>Rapor</h3>
    {df.to_html()}
    <br><a href="/indir">Excel indir</a>
    """

    return render_template_string(TEMPLATE,content=content)

@app.route("/indir")
def indir():
    return send_file("rapor.xlsx",as_attachment=True)

if __name__=="__main__":
    app.run()
