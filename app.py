from flask import Flask, request, send_file, jsonify
import astrologia
import pdf
import os
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('formulario.html')

@app.route('/api/mapa', methods=['POST'])
def gerar_e_enviar_mapa():
    try:
        # ===== CORREÇÃO APLICADA AQUI =====
        # Em vez de request.form, usamos request.get_json() para ler dados JSON
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Nenhum dado JSON recebido."}), 400

        # Acessa os dados do dicionário 'dados'
        nome = dados['nome']
        data_nasc = dados['data']
        hora_nasc = dados['hora']
        cidade = dados['cidade']
        estado = dados['estado']

        print(f"[DEBUG app.py] >>> Requisição recebida em /api/mapa.")
        print(f"[DEBUG app.py] Dados recebidos: Nome={nome}, Data={data_nasc}, Hora={hora_nasc}, Cidade={cidade}, Estado={estado}")

        # 2. Geração do mapa astral
        print("[DEBUG app.py] Chamando astrologia.gerar_mapa()...")
        mapa_data = astrologia.gerar_mapa(data_nasc, hora_nasc, cidade, estado)

        if mapa_data:
            # 3. Geração do PDF
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_filename = f"mapa_{nome.lower().replace(' ', '_')}_{timestamp}.pdf"
            
            print(f"[DEBUG app.py] Chamando pdf.criar_pdf()...")
            pdf.criar_pdf(nome, mapa_data, output_filename)
            
            print(f"[DEBUG app.py] PDF criado em: {output_filename}. Enviando arquivo...")
            return send_file(output_filename, as_attachment=True)
        else:
            print("[ERRO app.py] astrologia.gerar_mapa() retornou None.")
            return jsonify({"erro": "Não foi possível gerar os dados do mapa astral."}), 500

    except KeyError as e:
        # Este erro acontece se uma chave (ex: 'nome') estiver faltando no JSON
        return jsonify({"erro": f"Campo obrigatório ausente no JSON: {e.args[0]}"}), 400
    except Exception as e:
        print(f"[ERRO FATAL app.py] Ocorreu uma exceção não tratada: {repr(e)}")
        return jsonify({"erro": "Ocorreu um erro inesperado no servidor."}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)