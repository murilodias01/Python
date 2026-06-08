from flask import Blueprint, render_template, request, redirect, url_for
from modelos import db, Historico

# Criamos um Blueprint para organizar as rotas
calculadora_bp = Blueprint('calc', __name__)

@calculadora_bp.route('/', methods=['GET', 'POST'])
def home():
    resultado = None
    
    if request.method == 'POST':
        num1 = request.form.get('num1')
        num2 = request.form.get('num2')
        operacao = request.form.get('operacao')
        
        try:
            n1 = float(num1)
            n2 = float(num2)
            
            # Executa a operação matemática
            if operacao == 'soma':
                res = n1 + n2
                sinal = '+'
            elif operacao == 'subtracao':
                res = n1 - n2
                sinal = '-'
            elif operacao == 'multiplicacao':
                res = n1 * n2
                sinal = '*'
            elif operacao == 'divisao':
                if n2 == 0:
                    raise ZeroDivisionError
                res = n1 / n2
                sinal = '/'
            
            resultado = str(res)
            expressao_completa = f"{num1} {sinal} {num2}"
            
            # Guarda a operação no banco de dados (Model)
            nova_linha = Historico(expressao=expressao_completa, resultado=resultado)
            db.session.add(nova_linha)
            db.session.commit()
            
        except ZeroDivisionError:
            resultado = "Erro: Divisão por zero!"
        except (ValueError, TypeError):
            resultado = "Erro: Valores inválidos!"

    # Procura todo o histórico para exibir na View
    lista_historico = Historico.query.order_by(Historico.id.desc()).all()
    
    return render_template('calculadora.html', resultado=resultado, historico=lista_historico)

@calculadora_bp.route('/limpar', methods=['POST'])
def limpar_historico():
    # Rota extra para apagar o histórico se quiser
    db.session.query(Historico).delete()
    db.session.commit()
    return redirect(url_for('calc.home'))