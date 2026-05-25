from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calcular():
    resultado = None
    etapas = ""
    
    if request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            operacao = request.form['operacao']
            
            # Operações da calculadora
            if operacao == '+':
                resultado = num1 + num2
            elif operacao == '-':
                resultado = num1 - num2
            elif operacao == '*':
                resultado = num1 * num2
            elif operacao == '/':
                if num2 == 0:
                    return render_template('calculadora.html', etapas="Erro", resultado="Divisão por zero")
                resultado = num1 / division
                resultado = num1 / num2
                
            etapas = f'{num1} {operacao} {num2} ='
        except ValueError:
            resultado = "Erro"
            etapas = "Entrada inválida"

    return render_template('calculadora.html', etapas=etapas, resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)