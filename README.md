# 🔗 URL Shortener

API para encurtamento de URLs desenvolvida com Python e Flask.

## 🛠️ Tecnologias

- Python 3
- Flask
- SQLite
- Git & GitHub
- Postman

## ⚙️ Como rodar localmente

Instale as dependências:
```
pip install -r requirements.txt
```

Rode o servidor:
```
python app.py
```

O servidor vai rodar em: http://localhost:5000

## 📋 Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | /encurtar | Encurta uma URL |
| GET | /:codigo | Redireciona para a URL original |
| GET | /stats/:codigo | Retorna estatísticas do link |

## 📝 Exemplos de uso

**Encurtar uma URL:**
```
POST /encurtar
{
    "url": "https://github.com/gabriell-carmo"
}
```

**Resposta:**
```
{
    "codigo": "d22DG3",
    "url_curta": "http://localhost:5000/d22DG3",
    "url_original": "https://github.com/gabriell-carmo"
}
```

**Estatísticas de um link:**
```
GET /stats/d22DG3
```

**Resposta:**
```
{
    "acessos": 1,
    "codigo": "d22DG3",
    "criado_em": "2026-06-23 11:24:55",
    "url_original": "https://github.com/gabriell-carmo"
}
```

## ✅ Validações

- URL é obrigatória
- URL deve conter http:// ou https://
- Códigos inexistentes retornam erro 404

## 🗄️ Banco de Dados

O projeto usa SQLite. Na primeira execução o arquivo `urls.db` é criado automaticamente.

## 👨‍💻 Autor

Gabriel Carmo — [GitHub](https://github.com/gabriell-carmo) • [LinkedIn](https://linkedin.com/in/gabriell-carmo1)