from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Jogador(db.Model):
    __tablename__ = 'jogadores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    posicao = db.Column(db.String(50), nullable=False)
    clube = db.Column(db.String(100), nullable=False)
    cabeceio = db.Column(db.Integer, default=0)
    forca = db.Column(db.Integer, default=0)

    def __init__(self, nome, posicao, clube, cabeceio=0, forca=0):
        self.nome = nome
        self.posicao = posicao
        self.clube = clube
        self.cabeceio = cabeceio
        self.forca = forca