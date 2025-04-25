from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from zeep import Client
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# --- configuração de upload ---
UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- páginas estáticas ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fisico.html')
def fisico_page():
    return render_template('fisico.html')

@app.route('/ebook.html')
def ebook_page():
    return render_template('ebook.html')

@app.route('/audiolivro.html')
def audio_page():
    return render_template('audiolivro.html')

# --- SOAP dos Correios para cálculo de frete ---
WSDL_URL = 'https://soap.correios.com.br/Calculador/CalcPrecoPrazo.asmx?WSDL'
soap_client = Client(WSDL_URL)

@app.route('/calculate-shipping')
def calculate_shipping():
    cep_destino = request.args.get('cep', '').replace('-', '').strip()
    if len(cep_destino) != 8 or not cep_destino.isdigit():
        return jsonify({'erro': 'CEP inválido'}), 400

    resp = soap_client.service.CalcPrecoPrazo(
        nCdEmpresa='',
        sDsSenha='',
        nCdServico='04510',       # ajuste p/ PAC, Sedex, etc.
        sCepOrigem='01001000',    # seu CEP de origem (sem hífen)
        sCepDestino=cep_destino,
        nVlPeso=0.300,            # peso em kg
        nCdFormato=1,             # formato caixa
        nVlComprimento=20,        # cm
        nVlAltura=5,
        nVlLargura=15,
        nVlDiametro=0,
        sCdMaoPropria='N',
        nVlValorDeclarado=0,
        sCdAvisoRecebimento='N'
    )
    valor_str = resp.Servicos.cServico.Valor  # e.g. "12,50"
    valor_frete = float(valor_str.replace(',', '.'))
    return jsonify({'valor_frete': valor_frete})

# --- tratamento do envio do formulário físico ---
@app.route('/submit-physic', methods=['POST'])
def submit_physic():
    name         = request.form.get('name')
    email        = request.form.get('email')
    whatsapp     = request.form.get('whatsapp')
    street       = request.form.get('street')
    number       = request.form.get('number')
    complement   = request.form.get('complement')
    neighborhood = request.form.get('neighborhood')
    city         = request.form.get('city')
    state        = request.form.get('state')
    cep          = request.form.get('cep')
    receipt_file = request.files.get('receipt')

    if receipt_file:
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], receipt_file.filename)
        receipt_file.save(save_path)

    return render_template('success.html', name=name)

# --- envio do formulário e-Book ---
@app.route('/submit-ebook', methods=['POST'])
def submit_ebook():
    email = request.form.get('email')
    # aqui: enviar link de download por e-mail
    return render_template('success.html', name=email)

# --- envio do formulário Audiolivro ---
@app.route('/submit-audio', methods=['POST'])
def submit_audio():
    email = request.form.get('email')
    # aqui: enviar link do audiolivro por e-mail
    return render_template('success.html', name=email)

if __name__ == '__main__':
    app.run(debug=True)
