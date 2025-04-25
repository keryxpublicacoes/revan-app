from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from zeep import Client, Transport
from requests import Session
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# pasta de uploads para recibos
UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# rotas de páginas
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

# WSDL dos Correios
WSDL_URL = 'https://soap.correios.com.br/Calculador/CalcPrecoPrazo.asmx?WSDL'
soap_client = None

# cálculo de frete
@app.route('/calculate-shipping')
def calculate_shipping():
    cep = request.args.get('cep', '').replace('-', '').strip()
    if len(cep) != 8 or not cep.isdigit():
        return jsonify({'erro': 'CEP inválido'}), 400

    global soap_client
    try:
        if soap_client is None:
            session = Session()
            transport = Transport(session=session, timeout=10)
            soap_client = Client(WSDL_URL, transport=transport)
        resp = soap_client.service.CalcPrecoPrazo(
            nCdEmpresa='',
            sDsSenha='',
            nCdServico='04510',
            sCepOrigem='01001000',
            sCepDestino=cep,
            nVlPeso=0.300,
            nCdFormato=1,
            nVlComprimento=20,
            nVlAltura=5,
            nVlLargura=15,
            nVlDiametro=0,
            sCdMaoPropria='N',
            nVlValorDeclarado=0,
            sCdAvisoRecebimento='N'
        )
        valor_str = resp.Servicos.cServico.Valor  # ex: "12,50"
        frete = float(valor_str.replace(',', '.'))
    except Exception as e:
        app.logger.error(f'Erro ao calcular frete: {e}')
        frete = 10.00

    return jsonify({'valor_frete': frete})

# recebe e salva comprovante físico
@app.route('/submit-physic', methods=['POST'])
def submit_physic():
    receipt = request.files.get('receipt')
    if receipt:
        path = os.path.join(app.config['UPLOAD_FOLDER'], receipt.filename)
        receipt.save(path)
    return render_template('success.html')

# e-book
@app.route('/submit-ebook', methods=['POST'])
def submit_ebook():
    # aqui você pode salvar name, whatsapp e email
    return render_template('success.html')

# audiolivro
@app.route('/submit-audiolivro', methods=['POST'])
def submit_audiolivro():
    # aqui você pode salvar name, whatsapp e email
    return render_template('success.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
