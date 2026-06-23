import random
import string
import sqlite3
from flask import Flask, jsonify, request, redirect
from database import get_db, close_db, init_db

app = Flask(__name__)

app.teardown_appcontext(close_db)

def gerar_codigo(tamanho=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=tamanho))

@app.route('/encurtar', methods=['POST'])
def encurtar():
    dados = request.get_json()
    url = dados.get('url', '').strip()

    if not url:
        return jsonify({'erro': 'URL é obrigatória'}), 400

    codigo = gerar_codigo()
    db = get_db()
    db.execute('INSERT INTO urls (url_original, codigo) VALUES (?, ?)', (url, codigo))
    db.commit()

    return jsonify({
        'codigo': codigo,
        'url_curta': f'http://localhost:5000/{codigo}',
        'url_original': url
    }), 201

@app.route('/<codigo>')
def redirecionar(codigo):
    db = get_db()
    row = db.execute('SELECT * FROM urls WHERE codigo = ?', (codigo,)).fetchone()
    if row:
        db.execute('UPDATE urls SET acessos = acessos + 1 WHERE codigo = ?', (codigo,))
        db.commit()
        return redirect(row['url_original'])
    return jsonify({'erro': 'Código não encontrado'}), 404

@app.route('/stats/<codigo>')
def stats(codigo):
    db = get_db()
    row = db.execute('SELECT * FROM urls WHERE codigo = ?', (codigo,)).fetchone()
    if row:
        return jsonify({
            'url_original': row['url_original'],
            'codigo': row['codigo'],
            'acessos': row['acessos'],
            'criado_em': row['criado_em']
        })
    return jsonify({'erro': 'Código não encontrado'}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)