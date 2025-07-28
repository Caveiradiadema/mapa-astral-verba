from flask import Flask, request, send_file
from astrologia import gerar_mapa
from pdf import criar_pdf
import os

app = Flask(__name__)

@app.route("/api/mapa", methods=["POST"])
def gerar():
    nome = request.form.get('nome')
    data = request.form.get('data_nasc')
    hora = request.form.get('hora_nasc')
    cidade = request.form.get('cidade')
    estado = request.form.get('estado')

    mapa = gerar_mapa(data, hora, cidade, estado)
    if not mapa:
        return "Cidade não encontrada", 400

    filename = criar_pdf(mapa, nome)
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)