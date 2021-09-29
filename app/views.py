from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

# Create your views here.

listaPessoas = []


def index(request):
    return redirect('/adotar/')


def home(request):
    dados = {}
    if not listaPessoas:
        lerArquivo()

    dados['pessoas'] = listaPessoas
    return render(request, 'adotar/index.html', dados)


def lerArquivo():
    try:
        arq = open('db.txt', 'r+')
    except FileNotFoundError:
        arq = open('db.txt', 'w+')

    linhas = arq.readlines()
    count = 0
    while(count < len(linhas) // 5):
        pessoa = [
            str(linhas[5*count].strip()),
            str(linhas[5*count+1].strip()),
            str(linhas[5*count+2].strip()),
            str(linhas[5*count+4].strip()),
            str(linhas[5*count+3].strip())
        ]
        listaPessoas.append(pessoa)
        count += 1
    arq.close()


def detail(request, id=None):
    if not listaPessoas:
        lerArquivo()
    if id == None:
        id = request.GET['id']
        return redirect(id+'/')

    data = {}
    data['pessoa'] = search(id)
    data['id'] = id
    return render(request, 'adotar/detail.html', data)


def search(id):
    if not listaPessoas:
        lerArquivo()
    count = 0
    pessoa = ''
    while count < len(listaPessoas) and not pessoa:
        if listaPessoas[count][0] == str(id):
            pessoa = listaPessoas[count]
        count += 1
    return pessoa


def create(request):
    return render(request, 'adotar/create.html')


def edit(request, id):
    data = {}
    data['pessoa'] = search(id)
    return render(request, 'adotar/edit.html', data)


def update(request, id):
    pessoa = []
    if not listaPessoas:
        lerArquivo()
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
    atualizado = False
    while count < len(listaPessoas) and not atualizado:
        if listaPessoas[count][0] == str(id):
            listaPessoas[count] = pessoa[0]
        count += 1
    save()
    return redirect('home')


def remove(request, id):
    if not listaPessoas:
        lerArquivo()
    count = 0
    removido = False
    while count < len(listaPessoas) and not removido:
        if listaPessoas[count][0] == str(id):
            listaPessoas.remove(listaPessoas[count])
            removido = True
        count += 1
    save()
    return redirect('home')


def store(request):
    if not listaPessoas:
        ultimoId = 0
        lerArquivo()
    else:
        ultimoId = listaPessoas[-1][0]

    dados = request.POST

    pessoa = [
        str(int(ultimoId)+1),
        str(dados['nome']),
        str(dados['idade']),
        str(dados['cor']),
        str(dados['sexo'])
    ]
    listaPessoas.append(pessoa)
    save()
    result = 'Cadastro realizado com sucesso!'

    return redirect('home')


def save():
    arq = open('db.txt', 'w+')
    for [id, nome, idade, sexo, cor] in listaPessoas:
        arq.writelines(str(id)+'\n')
        arq.writelines(str(nome)+'\n')
        arq.writelines(str(idade)+'\n')
        arq.writelines(str(cor)+'\n')
        arq.writelines(str(sexo)+'\n')
    arq.close()
