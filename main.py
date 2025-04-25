from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from zeep import Client
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# pasta de uploads para recibos
UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# rota página inicial
@app.route('/')
def index():
    return render_template('index.html')

# rota compra livro físico
@app.route('/fisico')
def fisico():
    return render_template('fisico.html')

# rota compra e-book
@app.route('/ebook')
def ebook():
    return render_template('ebook.html')

# rota compra audiolivro
@app.route('/audiolivro')
def audiolivro():
    return render_template('audiolivro.html')

# WSDL dos Correios
WSDL_URL = 'https://soap.correios.com.br/Calculador/CalcPrecoPrazo.asmx?WSDL'
soap_client = Client(WSDL_URL)

# endpoint para cálculo de frete (stub fixo R$ 14,50)
@app.route('/calculate-shipping')
def calculate_shipping():
    # aqui simplesmente devolvemos o frete fixo
    frete = 14.50
    return jsonify({'valor_frete': frete})

# endpoint que recebe e salva o comprovante físico
@app.route('/submit-physic', methods=['POST'])
def submit_physic():
    receipt = request.files.get('receipt')
    if receipt:
        path = os.path.join(app.config['UPLOAD_FOLDER'], receipt.filename)
        receipt.save(path)
    return render_template('success.html')

# endpoints de e-book e audiolivro (simples)
@app.route('/submit-ebook', methods=['POST'])
def submit_ebook():
    return render_template('success.html')

@app.route('/submit-audiolivro', methods=['POST'])
def submit_audiolivro():
    return render_template('success.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
