# app.py  –  servidor Flask principal (VERSÃO FINAL CORRIGIDA)
# =============================================================
import os
import traceback
from flask import (Flask, request, jsonify, render_template,
                   send_from_directory)
from flask_cors import CORS

from astrologia import gerar_mapa_astral  # sua função de cálculo
from pdf import criar_pdf  # gera o PDF final

# ─────────────  Configuração básica  ──────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(BASE_DIR, "pdfs")

# --- CORREÇÃO APLICADA AQUI ---
# Definimos o caminho para a pasta 'templates'
TEMPL_DIR = os.path.join(BASE_DIR, "templates")

# O Flask precisa do caminho absoluto para `send_from_directory`
PDF_DIR_ABSOLUTE = os.path.abspath(PDF_DIR)

# --- E A CORREÇÃO É USADA AQUI ---
# Na inicialização do Flask, apontamos para a pasta de templates correta.
app = Flask(__name__, template_folder=TEMPL_DIR, static_folder="static")
CORS(app)  # permite chamadas JS locais sem CORS errors


# ─────────────  Rotas  ──────────────
@app.route("/", methods=["GET"])
def index():
    # Agora o Flask encontrará o 'formulario.html' dentro da pasta 'templates'
    return render_template("formulario.html")


@app.route("/api/mapa", methods=["POST"])
def api_mapa():
    """
    Endpoint que recebe dados JSON, GERA o PDF e DEVOLVE O ARQUIVO PDF
    diretamente na resposta.
    """
    try:
        data = request.get_json(force=True, silent=False)
        print("[DEBUG] Requisição recebida:", data)

        campos = ["nome", "data", "hora", "cidade", "estado"]
        if not all(k in data and data[k].strip() for k in campos):
            return jsonify({
                "sucesso": False,
                "erro": "Campos obrigatórios ausentes"
            }), 400

        mapa = gerar_mapa_astral(data["nome"].strip(), data["data"].strip(),
                                 data["hora"].strip(), data["cidade"].strip(),
                                 data["estado"].strip())
        if mapa is None:
            return jsonify({
                "sucesso": False,
                "erro": "Falha ao gerar dados do mapa"
            }), 500

        pdf_relpath = criar_pdf(mapa)
        pdf_filename = os.path.basename(pdf_relpath)

        return send_from_directory(PDF_DIR_ABSOLUTE,
                                   pdf_filename,
                                   as_attachment=True)

    except Exception as exc:
        print("[ERRO /api/mapa]", exc)
        traceback.print_exc()
        return jsonify({
            "sucesso": False,
            "erro": "Erro interno do servidor"
        }), 500


@app.route("/pdfs/<path:filename>")
def baixar_pdf(filename):
    """Serve arquivos PDF gerados em /pdfs."""
    return send_from_directory(PDF_DIR_ABSOLUTE, filename)


# ─────────────  Execução direta  ──────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
