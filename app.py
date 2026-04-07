from flask import Flask, render_template_string, request, redirect, send_file
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

KISILER = "kisiler.xlsx"
MODELLER = "modeller.xlsx"
BANTLAR = "bantlar.xlsx"
OPERASYON = "operasyonlar.xlsx"
DATA = "data.xlsx"

def init_files():
    if not os.path.exists(KISILER):
        pd.DataFrame(columns=["AdSoyad"]).to_excel(KISILER, index=False)
    if not os.path.exists(MODELLER):
        pd.DataFrame(columns=["Model"]).to_excel(MODELLER, index=False)
    if not os.path.exists(BANTLAR):
        pd.DataFrame(columns=["Bant"]).to_excel(BANTLAR, index=False)
    if not os.path.exists(OPERASYON):
        pd.DataFrame(columns=["Operasyon","Sure_sn"]).to_excel(OPERASYON, index=False)
    if not os.path.exists(DATA):
        pd.DataFrame(columns=["Tarih","AdSoyad","Model","Bant","Operasyon","Adet","Sure_sn"]).to_excel(DATA, index=False)

init_files()

@app.route("/")
def home():
    return render_template_string("""
    <h1>MAY SİSTEMİ</h1>
    <a href="/yonetim">Yönetim</a><br>
    <a href="/veri">Veri Giriş</a><br>
    <a href="/rapor">Rapor</a>
    """)

@app.route("/yonetim", methods=["GET","POST"])
def yonetim():
    if request.method == "POST":
        tip = request.form["tip"]
        veri = request.form["veri"]

        if veri.strip() == "":
            return redirect("/yonetim")

        if tip == "kisi":
            df = pd.read_excel(KISILER)
            df.loc[len(df)] = [veri]
            df.to_excel(KISILER, index=False)

        if tip == "model":
            df = pd.read_excel(MODELLER)
            df.loc[len(df)] = [veri]
            df.to_excel(MODELLER, index=False)

        if tip == "bant":
            df = pd.read_excel(BANTLAR)
            df.loc[len(df)] = [veri]
            df.to_excel(BANTLAR, index=False)

        if tip == "operasyon":
            sure = request.form["sure"]
            if sure.strip() != "":
                df = pd.read_excel(OPERASYON)
                df.loc[len(df)] = [veri, int(sure)]
                df.to_excel(OPERASYON, index=False)

    kisiler = pd.read_excel(KISILER)
    modeller = pd.read_excel(MODELLER)
    bantlar = pd.read_excel(BANTLAR)
    operasyon = pd.read_excel(OPERASYON)

    return render_template_string("""
    <h2>Yönetim</h2>

    <form method="post">
    <input name="veri" placeholder="Ad Soyad">
    <button name="tip" value="kisi">Kişi Ekle</button>
    </form>

    <form method="post">
    <input name="veri" placeholder="Model">
    <button name="tip" value="model">Model Ekle</button>
    </form>

    <form method="post">
    <input name="veri" placeholder="Bant">
    <button name="tip" value="bant">Bant Ekle</button>
    </form>

    <form method="post">
    <input name="veri" placeholder="Operasyon">
    <input name="sure" placeholder="Süre sn">
    <button name="tip" value="operasyon">Operasyon Ekle</button>
    </form>

    <h3>Kayıtlar</h3>
    {{kisiler.to_html()|safe}}
    {{modeller.to_html()|safe}}
    {{bantlar.to_html()|safe}}
    {{operasyon.to_html()|safe}}

    <a href="/">Ana Sayfa</a>
    """ , kisiler=kisiler, modeller=modeller, bantlar=bantlar, operasyon=operasyon)

@app.route("/veri", methods=["GET","POST"])
def veri():
    kisiler = pd.read_excel(KISILER)
    modeller = pd.read_excel(MODELLER)
    bantlar = pd.read_excel(BANTLAR)
    operasyon_df = pd.read_excel(OPERASYON)

    if request.method == "POST":
        kisi = request.form["kisi"]
        model = request.form["model"]
        bant = request.form["bant"]
        operasyon = request.form["operasyon"]
        adet = request.form["adet"]

        if "" in [kisi, model, bant, operasyon, adet]:
            return redirect("/veri")

        sure = operasyon_df[operasyon_df["Operasyon"] == operasyon]["Sure_sn"]
        if len(sure) == 0:
            return redirect("/veri")

        sure = int(sure.values[0])

        df = pd.read_excel(DATA)
        df.loc[len(df)] = [
            datetime.now().strftime("%Y-%m-%d"),
            kisi, model, bant, operasyon, int(adet), sure
        ]
        df.to_excel(DATA, index=False)

    data = pd.read_excel(DATA)

    return render_template_string("""
    <h2>Veri Giriş</h2>

    <form method="post">
    <input name="kisi" placeholder="Ad Soyad"><br>
    <input name="model" placeholder="Model"><br>
    <input name="bant" placeholder="Bant"><br>
    <input name="operasyon" placeholder="Operasyon"><br>
    <input name="adet" placeholder="Adet"><br>
    <button>Veri Gir</button>
    </form>

    <h3>Kayıtlar</h3>
    {{data.to_html()|safe}}

    <a href="/indir">Excel İndir</a><br>
    <a href="/">Ana Sayfa</a>
    """ , data=data)

@app.route("/indir")
def indir():
    return send_file(DATA, as_attachment=True)

@app.route("/rapor")
def rapor():
    df = pd.read_excel(DATA)

    if len(df) > 0:
        df["Performans %"] = (df["Adet"] * df["Sure_sn"]) / 32400 * 100

    return render_template_string("""
    <h2>Rapor</h2>
    {{df.to_html()|safe}}
    <a href="/">Ana Sayfa</a>
    """ , df=df)

if __name__ == "__main__":
    app.run()from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>MAY SİSTEMİ ÇALIŞIYOR 🚀</h1>"

if __name__ == "__main__":
    app.run()
