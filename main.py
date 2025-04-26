from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Configurações do servidor SMTP do Gmail
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'seminariokeryx@gmail.com'  # e-mail remetente
SMTP_PASSWORD = 'D@ny190709'         # você vai colocar sua senha normal aqui

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

# rota para cálculo de frete fixo
@app.route('/calculate-shipping')
def calculate_shipping():
    frete = 14.50
    return jsonify({'valor_frete': frete})

# função para envio de e-mail
def send_email_with_attachment(name, email_user, receipt_file):
    msg = EmailMessage()
    msg['Subject'] = f'Novo Pedido Revan - {name}'
    msg['From'] = SMTP_USER
    msg['To'] = 'keryxpublicacoes@gmail.com'

    msg.set_content(f'''
    Novo pedido recebido.

    Nome: {name}
    E-mail: {email_user}

    Anexo: Comprovante enviado.
    ''')

    if receipt_file:
        filename = receipt_file.filename
        file_data = receipt_file.read()
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=filename)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)

# rota para submissão física
@app.route('/submit-physic', methods=['POST'])
def submit_physic():
    name = request.form.get('name')
    email_user = request.form.get('email')
    receipt = request.files.get('receipt')

    send_email_with_attachment(name, email_user, receipt)

    return render_template('success.html')

# rota para submissão e-book
@app.route('/submit-ebook', methods=['POST'])
def submit_ebook():
    name = request.form.get('name')
    email_user = request.form.get('email')
    receipt = request.files.get('receipt')

    send_email_with_attachment(name, email_user, receipt)

    return render_template('success.html')

# rota para submissão audiolivro
@app.route('/submit-audiolivro', methods=['POST'])
def submit_audiolivro():
    name = request.form.get('name')
    email_user = request.form.get('email')
    receipt = request.files.get('receipt')

    send_email_with_attachment(name, email_user, receipt)

    return render_template('success.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
