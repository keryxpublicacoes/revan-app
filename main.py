from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import base64
import requests

app = Flask(__name__, static_folder='static')
CORS(app)

UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

APPS_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbx_jVZf6hPHqg10xgfylug9z6_da-ECfaWy2SsaCYw3r5C4YC1Vqo01R8M7KhE3Wvv7/exec'

# --- rotas de página ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fisico')
def fisico():
    return render_template('fisico.html')

@app.route('/ebook')
def ebook():
    return render_template('ebook.html')

@app.route('/audiolivro')
def audiolivro():
    return render_template('audiolivro.html')

# --- frete fixo R$14,50 ---
@app.route('/calculate-shipping')
def calculate_shipping():
    frete = 14.50
    return jsonify({'valor_frete': frete})

# --- formulários ---
@app.route('/submit-physic', methods=['POST'])
def submit_physic():
    return process_submission('fisico')

@app.route('/submit-ebook', methods=['POST'])
def submit_ebook():
    return process_submission('ebook')

@app.route('/submit-audiolivro', methods=['POST'])
def submit_audiolivro():
    return process_submission('audiolivro')

def process_submission(tipo):
    # Captura os campos do formulário
    data = {
        'type': tipo,
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        'whatsapp': request.form.get('whatsapp'),
    }

    if tipo == 'fisico':
        data.update({
            'street': request.form.get('street'),
            'number': request.form.get('number'),
            'complement': request.form.get('complement'),
            'neighborhood': request.form.get('neighborhood'),
            'city': request.form.get('city'),
            'state': request.form.get('state'),
            'cep': request.form.get('cep'),
            'shipping': request.form.get('shipping'),
            'total': request.form.get('total'),
        })

    # Captura e converte o comprovante para base64
    receipt = request.files.get('receipt')
    if receipt:
        receipt_stream = receipt.read()
        receipt_base64 = base64.b64encode(receipt_stream).decode('utf-8')
        data['receipt'] = receipt_base64

    # Envia para o Apps Script
    response = requests.post(APPS_SCRIPT_URL, data=data)

    # Retorna a resposta que o Apps Script gerar
    return response.text

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
