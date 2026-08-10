from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify

app = Flask(__name__)
app.secret_key = "segredo123"

# BANCO DE DADOS

@app.route("/filtrar/<status>")
def filtrar(status):

    if "usuario" not in session:
        return jsonify([])

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, titulo, descricao, status
        FROM tarefas
        WHERE usuario_id=? AND status=?
    """, (session["usuario"], status))

    tarefas = cursor.fetchall()

    conn.close()

    resultado = []

    for t in tarefas:
        resultado.append({
            "id": t[0],
            "titulo": t[1],
            "descricao": t[2],
            "status": t[3]
        })

    return jsonify(resultado)
def conectar():
    return sqlite3.connect("banco.db")

@app.route("/dados_grafico")
def dados_grafico():

    if "usuario" not in session:
        return jsonify({})

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM tarefas
        WHERE usuario_id=?
        GROUP BY status
    """, (session["usuario"],))

    dados = cursor.fetchall()

    conn.close()

    resultado = {
        "Pendente": 0,
        "Em andamento": 0,
        "Concluída": 0
    }

    for status, qtd in dados:
        resultado[status] = qtd

    return jsonify(resultado)


@app.route("/progresso")
def progresso():

    if "usuario" not in session:
        return redirect("/login")

    return render_template("progresso.html")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT UNIQUE,
        senha TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        descricao TEXT,
        status TEXT,
        usuario_id INTEGER
    )
    """)

    conn.commit()
    conn.close()

criar_tabelas()

# LOGIN

@app.route("/")
def inicio():
    return redirect("/login")


@app.route("/registro", methods=["GET","POST"])
def registro():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        senha = generate_password_hash(request.form["senha"])

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO usuarios(nome,email,senha) VALUES(?,?,?)",
            (nome,email,senha)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("registro.html")


@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE email=?",
            (email,)
        )

        usuario = cursor.fetchone()

        conn.close()

        if usuario and check_password_hash(usuario[3], senha):
            session["usuario"] = usuario[0]
            session["nome"] = usuario[1]
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# DASHBOARD

@app.route("/dashboard")
def dashboard():

    if "usuario" not in session:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tarefas WHERE usuario_id=?",
        (session["usuario"],)
    )

    tarefas = cursor.fetchall()

    conn.close()

    frase = ""

    try:
        resposta = requests.get(
            "https://api.adviceslip.com/advice"
        )

        frase = resposta.json()["slip"]["advice"]

    except:
        frase = "Tenha um ótimo dia!"

    return render_template(
        "dashboard.html",
        tarefas=tarefas,
        frase=frase
    )

# NOVA TAREFA

@app.route("/nova_tarefa", methods=["GET","POST"])
def nova_tarefa():

    if "usuario" not in session:
        return redirect("/login")

    if request.method == "POST":

        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        status = request.form["status"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO tarefas
        (titulo,descricao,status,usuario_id)
        VALUES (?,?,?,?)
        """,(titulo,descricao,status,session["usuario"]))

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("nova_tarefa.html")

# EDITAR

@app.route("/editar/<int:id>", methods=["GET","POST"])
def editar(id):

    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":

        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        status = request.form["status"]

        cursor.execute("""
        UPDATE tarefas
        SET titulo=?, descricao=?, status=?
        WHERE id=?
        """,(titulo,descricao,status,id))

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    cursor.execute(
        "SELECT * FROM tarefas WHERE id=?",
        (id,)
    )

    tarefa = cursor.fetchone()

    conn.close()

    return render_template(
        "editar_tarefa.html",
        tarefa=tarefa
    )

# EXCLUIR

@app.route("/excluir/<int:id>")
def excluir(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tarefas WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/progresso")
def pagina_progresso(): 
    if "usuario" not in session:
        return redirect("/login")
    return render_template("progresso.html")

if __name__ == "__main__":
    app.run(debug=True)