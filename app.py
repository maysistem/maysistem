from flask import Flask, render_template_string, request, redirect, send_file
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

DATA = "data.xlsx"

if not os.path.exists(DATA):
    pd.DataFrame(columns=["Tarih","Kisi","Model","Bant","Operasyon","Adet"]).to_excel(DATA, index=False)

@app.route("/", methods=["GET","POST"])
def home():
    df = pd.read_excel(DATA)

    arama = request.args.get("arama")

    if arama:
        df = df[df.apply(lambda x: x.astype(str).str.contains(arama).any(), axis=1)]

    table = df.to_html()

    return render_template_string("""
    <h1>MAY SİSTEMİ</h1>

    <form method="get">
        <input name="arama" placeholder="Ara...">
        <button>Ara</button>
    </form>

    <form method="post">
        <input name="kisi" placeholder="Kişi"><br>
        <input name="model" placeholder="Model"><br>
        <input name="bant" placeholder="Bant"><br>
        <input name="operasyon" placeholder="Operasyon"><br>
        <input name="adet" placeholder="Adet"><br>
        <button>Kaydet</button>
    </form>

    <h3>Kayıtlar</h3>
    """ + table + """

    <h3>Tarih ile indir</h3>
    <form action="/indir">
        <input name="tarih" placeholder="2026-04-07">
        <button>Excel indir</button>
    </form>
    """)

@app.route("/", methods=["POST"])
def ekle():
    df = pd.read_excel(DATA)

    df.loc[len(df)] = [
        datetime.now().strftime("%Y-%m-%d"),
        request.form["kisi"],
        request.form["model"],
        request.form["bant"],
        request.form["operasyon"],
        int(request.form["adet"])
    ]

    df.to_excel(DATA, index=False)
    return redirect("/")

@app.route("/indir")
def indir():
    tarih = request.args.get("tarih")
    df = pd.read_excel(DATA)

    if tarih:
        df = df[df["Tarih"] == tarih]

    dosya = "filtre.xlsx"
    df.to_excel(dosya, index=False)

    return send_file(dosya, as_attachment=True)

if __name__ == "__main__":
    app.run()
