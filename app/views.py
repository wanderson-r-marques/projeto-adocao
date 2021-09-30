from django.shortcuts import render     # Biblioteca para redenrizar as views
from django.shortcuts import redirect   # Biblioteca para redirecionar as views


# Create your views here.

listaPessoas = []   # Lista que vai receber os dados do arquivo db.txt


def index(request):  # Função que redireciona para página principal
    return redirect('/adotar/')


def home(request):  # Função que redireciona para a Home
    dados = {}  # Lista vazia
    if not listaPessoas:  # Verifica se a lista tá vazia
        lerArquivo()    # Se a lista estiver vazia chama a função para popular

    # Atribui a lista aos dados a serem passados para a view
    dados['pessoas'] = listaPessoas
    return render(request, 'adotar/index.html', dados)  # Chama a view index


def lerArquivo():  # Função para popular a lista
    try:
        arq = open('db.txt', 'r+')  # Abre o arquivo caso exista
    except FileNotFoundError:
        arq = open('db.txt', 'w+')  # Cria o arquivo e abre

    linhas = arq.readlines()    # Pega todas as linhas do arquivo
    count = 0
    while(count < len(linhas) // 5):  # Loop para criar a lista com os dados
        pessoa = [
            str(linhas[5*count].strip()),
            str(linhas[5*count+1].strip()),
            str(linhas[5*count+2].strip()),
            str(linhas[5*count+4].strip()),
            str(linhas[5*count+3].strip())
        ]
        listaPessoas.append(pessoa)  # Popula a lista com os dados do arquivo
        count += 1
    arq.close()  # Fecha o arquivo


def detail(request, id=''):  # Função para exibir os detalhes da pessoa
    if not listaPessoas:    # Verifica se lista está vazia
        lerArquivo()    # Função para preencher a lista
    if id == '':    # Verifica se o id está vazio
        id = request.GET['id']  # Pega o ID do GET
        return redirect(id+'/')  # Redireciona para URL de detalhes

    data = {}  # Cria um dicionário vazio
    # Usa a função search para buscar a pessoa pelo ID
    # Usa a função search para pegar a pessoa pelo ID
    data['pessoa'] = search(id)
    data['id'] = id
    # Abre a view detalhes passando data
    return render(request, 'adotar/detail.html', data)


def search(id):  # Função para pegar o registro pelo ID
    if not listaPessoas:    # Verifica se a lista está vazia
        lerArquivo()    # Preenche a lista
    count = 0
    pessoa = ''
    # Loop para encontra a pessoa na lista
    while count < len(listaPessoas) and not pessoa:
        if listaPessoas[count][0] == str(id):
            pessoa = listaPessoas[count]
        count += 1
    return pessoa


def create(request):    # Função para abrir a tela de cadastro
    return render(request, 'adotar/create.html')


def store(request):  # Função que cadastra a pessoa
    if not listaPessoas:
        lerArquivo()
        ultimoId = 0  # Se estiver vazia o último ID rececbe zero
    else:
        ultimoId = listaPessoas[-1][0]  # Se não estiver vazia pega últimoID

    dados = request.POST    # Pega os dados via post

    pessoa = [  # Cria o array da pessoa
        str(int(ultimoId)+1),
        str(dados['nome']),
        str(dados['idade']),
        str(dados['cor']),
        str(dados['sexo'])
    ]

    listaPessoas.append(pessoa)  # Acrescenta a pessoa na lista
    save()
    return redirect('home')


def edit(request, id):  # Função para abrir a tela de editar
    data = {}
    data['pessoa'] = search(id)  # Pegar a pessoa usando o ID
    return render(request, 'adotar/edit.html', data)    # Abre a view de editar


def update(request, id):    # Função para atualizar a pessoa
    pessoa = []  # Cria lista vazia
    if not listaPessoas:    # Verifica se lista tá vazia
        lerArquivo()    # Preenche a lista
    dados = request.POST
    newDatas = [
        str(id),
        str(dados['nome']),
        str(dados['idade']),
        str(dados['cor']),
        str(dados['sexo'])
    ]
    pessoa.append(newDatas)
    count = 0
    atualizado = False  # Faz um loop para acha a pessoa
    while count < len(listaPessoas) and not atualizado:
        if listaPessoas[count][0] == str(id):   # Verifica se achou
            listaPessoas[count] = pessoa[0]  # Atualiza na lista
        count += 1
    save()  # Função para salvar no arquivo
    return redirect('home')  # AbreRedireciona para a home


def remove(request, id):    # Função para remover a pessoa
    if not listaPessoas:    # Verifica se a lista está vazia
        lerArquivo()    # Preenche a lista
    count = 0
    removido = False  # Faz um loop para achar a pessoa
    while count < len(listaPessoas) and not removido:
        if listaPessoas[count][0] == str(id):   # Se a pessoa foi encontrada
            # Remove a pessoa da lista
            listaPessoas.remove(listaPessoas[count])
            removido = True
        count += 1
    save()  # Salva no arquivo
    return redirect('home')


def save():  # Função usada para salvar no arquivo
    arq = open('db.txt', 'w+')  # Abrir o arquivo
    for [id, nome, idade, sexo, cor] in listaPessoas:   # Loop para salvar os dados
        arq.writelines(str(id)+'\n')
        arq.writelines(str(nome)+'\n')
        arq.writelines(str(idade)+'\n')
        arq.writelines(str(cor)+'\n')
        arq.writelines(str(sexo)+'\n')
    arq.close()  # Fecha o arquivo
