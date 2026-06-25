import random
import string
from urllib.parse import urlparse
from flask import Flask, jsonify, request, redirect
from database import get_db, close_db, init_db

app = Flask(__name__)
app.teardown_appcontext(close_db)


def gerar_codigo(tamanho=6):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=tamanho))


def url_valida(url):
    try:
        resultado = urlparse(url)
        return all([resultado.scheme in ['http', 'https'], resultado.netloc])
    except Exception:
        return False


def buscar_url(db, codigo):
    return db.execute(
        'SELECT * FROM urls WHERE codigo = ?', (codigo,)
    ).fetchone()


@app.route('/encurtar', methods=['POST'])
def encurtar():
    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'Corpo da requisição inválido'}), 400

    url = dados.get('url', '').strip()

    if not url:
        return jsonify({'erro': 'URL é obrigatória'}), 400

    if not url_valida(url):
        return jsonify({'erro': 'URL inválida. Use http:// ou https://'}), 400

    codigo = gerar_codigo()
    db = get_db()
    db.execute(
        'INSERT INTO urls (url_original, codigo) VALUES (?, ?)',
        (url, codigo)
    )
    db.commit()

    return jsonify({
        'codigo': codigo,
        'url_curta': f'http://localhost:5000/{codigo}',
        'url_original': url
    }), 201


@app.route('/<codigo>')
def redirecionar(codigo):
    db = get_db()
    row = buscar_url(db, codigo)

    if not row:
        return jsonify({'erro': 'Código não encontrado'}), 404

    db.execute(
        'UPDATE urls SET acessos = acessos + 1 WHERE codigo = ?',
        (codigo,)
    )
    db.commit()
    return redirect(row['url_original'])


@app.route('/stats/<codigo>')
def stats(codigo):
    db = get_db()
    row = buscar_url(db, codigo)

    if not row:
        return jsonify({'erro': 'Código não encontrado'}), 404

    return jsonify({
        'url_original': row['url_original'],
        'codigo': row['codigo'],
        'acessos': row['acessos'],
        'criado_em': row['criado_em']
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({'erro': 'Rota não encontrada'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'erro': 'Erro interno do servidor'}), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=True)