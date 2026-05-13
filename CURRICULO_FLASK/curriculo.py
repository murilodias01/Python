from flask import Flask, render_template_string

app = Flask(__name__)

# 1. Base de dados simulada em Python
dados_curriculo = {
    "pessoal": {
        "nome": "Murilo Dias",
        "telefone": "(11) 99999-0000",
        "email": "murilodias2803@gmail.com",
    },
    "educacao": [
        {
            "instituicao": "Universidade XYZ",
            "curso": "Ciência da Computação",
            "conclusao": "2023",
        },
        {
            "instituicao": "Escola Técnica ABC",
            "curso": "Técnico em Informática",
            "conclusao": "2019",
        },
    ],
    "experiencia": [
        {
            "cargo": "Desenvolvedor Júnior",
            "empresa": "Tech Solutions",
            "periodo": "2023 - Presente",
            "detalhes": "Desenvolvimento de APIs com Flask.",
        },
        {
            "cargo": "Estagiário",
            "empresa": "WebData",
            "periodo": "2022 - 2023",
            "detalhes": "Manutenção de sites corporativos.",
        },
    ],
    "cursos": [
        "Python Avançado - Udemy",
        "Flask Web Development - Alura",
        "Docker Essentials",
    ],
    "idiomas": {"ingles": "Avançado (C1)", "espanhol": "Intermediário (B2)"},
}

# 2. Template HTML estruturado como string Python
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Currículo - {{ dados.pessoal.nome }}</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; margin: 40px; color: #333; background-color: #f9f9f9; }
        .container { max-width: 800px; margin: auto; background: #fff; padding: 40px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; margin-bottom: 5px; font-size: 2.5em; }
        h2 { color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 5px; margin-top: 30px; }
        .contato { color: #7f8c8d; font-size: 1.1em; margin-bottom: 30px; }
        .item { margin-bottom: 20px; }
        .titulo-item { font-weight: bold; color: #2c3e50; }
        .subtitulo-item { font-style: italic; color: #7f8c8d; }
        ul { padding-left: 20px; }
        li { margin-bottom: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{{ dados.pessoal.nome }}</h1>
            <p class="contato">📞 {{ dados.pessoal.telefone }} | ✉️ {{ dados.pessoal.email }}</p>
        </header>

        <section>
            <h2>Experiência de Trabalho</h2>
            {% for exp in dados.experiencia %}
            <div class="item">
                <span class="titulo-item">{{ exp.cargo }}</span> — <span class="subtitulo-item">{{ exp.empresa }}</span>
                <br><small>{{ exp.periodo }}</small>
                <p>{{ exp.detalhes }}</p>
            </div>
            {% endfor %}
        </section>

        <section>
            <h2>Escolas / Formação Acadêmica</h2>
            {% for edu in dados.educacao %}
            <div class="item">
                <span class="titulo-item">{{ edu.curso }}</span>
                <br><span class="subtitulo-item">{{ edu.instituicao }} (Conclusão: {{ edu.conclusao }})</span>
            </div>
            {% endfor %}
        </section>

        <section>
            <h2>Cursos Extra-curriculares</h2>
            <ul>
                {% for curso in dados.cursos %}
                <li>{{ curso }}</li>
                {% endfor %}
            </ul>
        </section>

        <section>
            <h2>Proficiência em Idiomas</h2>
            <ul>
                <li><strong>Inglês:</strong> {{ dados.idiomas.ingles }}</li>
                <li><strong>Espanhol:</strong> {{ dados.idiomas.espanhol }}</li>
            </ul>
        </section>
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, dados=dados_curriculo)


if __name__ == "__main__":
    app.run(debug=True)
