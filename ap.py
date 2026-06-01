import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Inicialização do Flask
app = Flask(__name__)

# Configuração do Banco de Dados SQLite
# Define o caminho para o arquivo alunos.db na mesma pasta do projeto
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(base_dir, 'alunos.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do SQLAlchemy ligado ao app
db = SQLAlchemy(app)

# ==========================================
# MODEL (Tabela de Alunos)
# ==========================================
class Aluno(db.Model):
    __tablename__ = 'alunos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    # [Exercício 1] Campo telefone adicionado
    telefone = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"<Aluno {self.nome}>"


# ==========================================
# ROTAS (CRUD)
# ==========================================

# ROTA: Listar alunos (Read)
@app.route('/')
def lista():
    # [Exercício 2] Ordenado por ID decrescente
    # [Exercício 3] .count() para saber o total de alunos
    alunos = Aluno.query.order_by(Aluno.id.desc()).all()
    total_alunos = Aluno.query.count() 
    
    return render_template('lista.html', alunos=alunos, total=total_alunos)


# ROTA: Cadastrar aluno (Create - GET e POST)
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone') # [Exercício 1]
        
        # Cria o objeto e salva no banco
        novo_aluno = Aluno(nome=nome, email=email, telefone=telefone)
        db.session.add(novo_aluno)
        db.session.commit()
        
        return redirect(url_for('lista'))
        
    return render_template('formulario.html', aluno=None)


# ROTA: Editar aluno (Update - GET e POST)
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    aluno = Aluno.query.get_or_404(id)
    
    if request.method == 'POST':
        aluno.nome = request.form.get('nome')
        aluno.email = request.form.get('email')
        aluno.telefone = request.form.get('telefone') # [Exercício 1]
        
        db.session.commit() # Grava a alteração
        return redirect(url_for('lista'))
        
    return render_template('formulario.html', aluno=aluno)


# ROTA: Excluir aluno (Delete - POST)
@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    return redirect(url_for('lista'))


# ==========================================
# EXECUÇÃO DO APP
# ==========================================
if __name__ == '__main__':
    # Cria as tabelas caso elas não existam antes de rodar o servidor
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)