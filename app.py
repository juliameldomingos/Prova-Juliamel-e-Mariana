from flask import Flask, render_template, request

app=Flask (__name__)

@app.route('/', methods=['GET', 'POST'])
def calculadora_imc():
    """rota principal calculadora"""
    erros =[]
    resultado= None
    dados_form= {
        'nome': '',
        'peso': '',
        'altura': '',
    }

    if request.method == 'POST':
#Recebe os dados enviandos e remove espaços em branco
        nome_str = request.form.get('nome', '').strip()
        peso_str = request.form.get('peso', '').strip()
        altura_str = request.form.get('altura', '').strip()

    #mantei os valos digitados caso de erro
        dados_form['nome'] = nome_str
        dados_form['peso'] = peso_str
        dados_form['altura'] = altura_str

        nome = None
        peso = None
        altura = None
        
        #campo nome
        if not nome_str:
            erros.append('Informe o nome.')
        else:
            nome = nome_str

        #campo peso
        if not peso_str:
            erros.append('Informe o peso.')
        else:
            try:
                peso = float(peso_str.replace(',','.'))
                if peso <= 0 or peso > 300:
                    erros.append('o peso deve ser maior que 0 ate 300.')
            except ValueError:
                    erros.append('O peso deve ser um valor numérico válido.')

        #campo altura
        if not altura_str:
                erros.append('Informe a altura')
        else:
            try:
                altura=float(altura_str.replace(',','.'))
                if altura <0.5 or altura >2.5:
                    erros.append('A altura deve estar entre 0,5 e 2,5')
            except ValueError:
                erros.append('A altura deve ser um valor numérico válido')

            
                #calculo e classificação se não houver erros de validação
                if not erros:
                    imc = peso / (altura ** 2)
                    imc_arredondado = round (imc, 2)
                
                #classifição por faixas usando if/elif/else
                if imc_arredondado < 18.5:
                    faixa ='abaixo do peso'
                    classe_alerta ='alert-info'
                    icone = '🔵'
                elif imc_arredondado < 25.0:
                    faixa ='peso normal'
                    classe_alerta ='alert-success'
                    icone = '🟢'
                elif imc_arredondado < 30.0:
                    faixa ='sobrepeso'
                    classe_alerta ='alert-warning'
                    icone = '🟡'
                else:
                    faixa ='obesidade'
                    classe_alerta ='alert-danger'
                    icone = '🔴'
                
                #prepara dos dados para exibir o resultado com as cores
                resultado = {
                    'nome': nome,
                    'peso': peso,
                    'altura': altura,
                    'imc': imc_arredondado,
                    'faixa': faixa,
                    'classe_alerta': classe_alerta,
                    'icone': icone
                }

            #Rederiza o index.htlm passando erros, resultadops e dados

    return render_template(
        'index.html',
        erros = erros,
        resultado = resultado,
        dados_form = dados_form
    )

@app.route('/equipe')
def pagina_equipe():
    """Pagina de apresentacao da equipe do projeto."""
    return render_template('equipe.html')

if __name__ == '__main__':
    app.run(debug=True)
                
