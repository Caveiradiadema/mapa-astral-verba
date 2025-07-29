from flask import Flask, request, send_file, render_template, send_from_directory
from astrologia import gerar_mapa
from pdf import criar_pdf
import os
from datetime import datetime

app = Flask(__name__, template_folder='.')

@app.route("/", methods=["GET"])
def home():
    return render_template("formulario.html")

# Rota para servir a logo diretamente a partir do diretório do projeto.
@app.route('/logo.png')
def serve_logo():
    """Serve o arquivo logo.png localizado no mesmo diretório deste script.

    O formulário HTML referencia /logo.png para a imagem de logomarca. Sem esta
    rota, o servidor Flask retornaria 404, pois não há pasta static. Ao
    adicionar esta rota, garantimos que a imagem seja servida corretamente
    independentemente da localização do diretório de trabalho.
    """
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'logo.png')

@app.route("/api/mapa", methods=["POST"])
def gerar():
    try:
        print("\n[DEBUG app.py] >>> Requisição recebida em /api/mapa.")
        nome = request.form.get('nome')
        data = request.form.get('data_nasc')
        hora = request.form.get('hora_nasc')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')

        if data and len(data) == 8 and "/" not in data:
            data = f"{data[:2]}/{data[2:4]}/{data[4:]}"
        if hora and len(hora) == 4 and ":" not in hora:
            hora = f"{hora[:2]}:{hora[2:]}"

        print(f"[DEBUG app.py] Dados recebidos: Nome={nome}, Data={data}, Hora={hora}, Cidade={cidade}, Estado={estado}")
        print("[DEBUG app.py] Chamando astrologia.gerar_mapa()...")
        
        mapa = gerar_mapa(data, hora, cidade, estado)
        
        if not mapa:
            print("[ERRO app.py] gerar_mapa() retornou None.")
            return "Erro ao gerar os dados do mapa. Verifique o console do servidor.", 400

        print(f"[DEBUG app.py] Mapa recebido de gerar_mapa(): {mapa}")
        print("[DEBUG app.py] Chamando pdf.criar_pdf()...")
        
        output_path = f"mapa_{nome.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        criar_pdf(nome, mapa, output_path)
        
        print(f"[DEBUG app.py] PDF criado em: {output_path}. Enviando arquivo...")
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print(f"[ERRO CRÍTICO em app.py] {repr(e)}")
        return f"Erro crítico no servidor: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)