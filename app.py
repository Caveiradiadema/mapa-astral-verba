from flask import Flask, request, send_file, jsonify
import astrologia
import pdf
import os
from datetime import datetime
import traceback # Importa a biblioteca de traceback

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('formulario.html')

@app.route('/api/mapa', methods=['POST'])
def gerar_e_enviar_mapa():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Nenhum dado JSON recebido."}), 400

        nome = dados['nome']
        data_nasc = dados['data']
        hora_nasc = dados['hora']
        cidade = dados['cidade']
        estado = dados['estado']

        print(f"[DEBUG app.py] >>> Requisição recebida em /api/mapa.")
        print(f"[DEBUG app.py] Dados recebidos: Nome={nome}, Data={data_nasc}, Hora={hora_nasc}, Cidade={cidade}, Estado={estado}")

        mapa_data = astrologia.gerar_mapa(data_nasc, hora_nasc, cidade, estado)

        if mapa_data:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_filename = f"mapa_{nome.lower().replace(' ', '_')}_{timestamp}.pdf"
            
            pdf.criar_pdf(nome, mapa_data, output_filename)
            
            print(f"[DEBUG app.py] PDF criado em: {output_filename}. Enviando arquivo...")
            return send_file(output_filename, as_attachment=True)
        else:
            print("[ERRO app.py] astrologia.gerar_mapa() retornou None. Verifique os logs de astrologia.py para mais detalhes.")
            return jsonify({"erro": "Não foi possível gerar os dados do mapa astral. Causa provável: localização não encontrada ou dados inválidos."}), 500

    except KeyError as e:
        print(f"[ERRO app.py] Campo obrigatório ausente no JSON: {e.args[0]}")
        return jsonify({"erro": f"Campo obrigatório ausente no JSON: {e.args[0]}"}), 400
    except Exception as e:
        # ===== CÓDIGO APRIMORADO AQUI =====
        # Imprime o erro completo e o traceback para o log
        full_traceback = traceback.format_exc()
        print(f"[ERRO FATAL app.py] Ocorreu uma exceção não tratada: {repr(e)}")
        print("--- INÍCIO DO TRACEBACK ---")
        print(full_traceback)
        print("--- FIM DO TRACEBACK ---")
        return jsonify({"erro": "Ocorreu um erro inesperado no servidor."}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)