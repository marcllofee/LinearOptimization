###################################################################################################################
#Pacotes importados
import math
import sys 
import numpy as np
from numpy import linalg
from numpy import append

#Entrada de dados obrigatórios
m = int(input('Digite o número de restrições: '))
n = int(input('Digite o número de variáveis: '))
A = []
b = []
c = []

B = [] #Matriz básica
N = [] #Matriz não básica

###################################################################################################################
#Funções que serão usadas
def entradas(m,n):              #Recebe o num de restrição e de variáveis e gera os vetores b e c e a matriz A
    for i in range(0,m):        #Construir a matriz A
        linhai = []
        for j in range(0,n):
            z = float(input('Digite a posição {}: '.format((i+1,j+1))))
            linhai.append(z)
        A.append(linhai)
    
    for i in range (0, n):      #Construir o vetor de custo c
        c.append(float(input('Digite a componente {} do vetor de custo: '.format(i+1))))

    for i in range (0, m):      #Construir o vetor de var indep b
        b.append(float(input('Digite a componente {} do vetor de var. indep.: '.format(i+1))))

def dict_values(dict):
    teste = []
    for i in dict.values():
        teste.append(i)
    return teste

def dict_keys(dict):
    teste = []
    for i in dict.keys():
        teste.append(i)
    return teste

def metodo(A,vb,vn,c,b):
    B = []
    cb = []
    N = []
    cn = []

    for i in vb:
        B.append(A[:,i-1])
    for i in vn:
        N.append(A[:,i-1])
    for i in vb:
        cb.append(c[i-1])
    for i in vn:
        cn.append(c[i-1])
    
    B = np.transpose(np.array(B))
    N = np.transpose(np.array(N))
    cb = np.transpose(np.array(cb))
    cn = np.transpose(np.array(cn))
    
    xb = linalg.solve(B,b)

    Bt = np.transpose(B)
    vetmult = linalg.solve(Bt,cb)
    custosrel = cn - np.transpose((vetmult @ N))
    
    custosrelmin = custosrel.min()
    aux = custosrel.tolist()
    indcustosrelmin = aux.index(custosrelmin)

    #Condição de parada numero 2
    if custosrelmin < 0:
        y = linalg.solve(B,N[:,indcustosrelmin])
        if y.max() <= 0:
            print('O PROBLEMA É ILIMITADO!!')
            sys.exit()
        
        posep = []
        valep =[]
        eppos = {}
        for i in range(0,len(xb)):
            if y[i] > 0:
                ep = xb[i]/y[i]
                #eppos.append((ep,i+1))
                eppos[i] = ep
                posep.append(ep)

        posep = dict_keys(eppos)
        valep = dict_values(eppos)
        epmin = min(valep)
        posepmin = valep.index(epmin)
        posicao = posep[posepmin]               #Posição que vai sair da base

        #Atualizar a base e não-base
        auxvb = vb
        auxvn = vn

        sair = vb[posicao]
        entrar = vn[indcustosrelmin]

        vb[posicao] = entrar
        vn[indcustosrelmin] = sair

        metodo(A,vb,vn,c,b)
    else:
        #Estamos na solução ótima
        fxb = xb@cb
        fxblist.append(fxb)
        #print(f'A solução ótima é dada em: {xb}')
        #print(f'O valor ótimo é f(xb) = {fxb}')
    
    fxbk = fxblist[0]
    return (fxbk,xb)

def fase1(A,m,n,b):
    vb = []
    vn = []
    c = []
    I = np.eye(m)
    for i in range(n,n+m): #(6,8)
        vb.append(i+1)
    for i in range(0,n):
        vn.append(i+1)
    for i in range(0,n+m):
        if i < n:
            c.append(0)
        else:
            c.append(1)
    Ab = np.concatenate((A, I),axis = 1)

    yotimo = metodo(Ab,vb,vn,c,b)[0]
    
    if yotimo != 0:
        print('O problema é infactivel!!')
        sys.exit()
    else:
        vnaux = vn.copy()
        for i in range(0, len(vn)):
            if vn[i] > n:
                vnaux.remove(vn[i])
        return vb,vnaux

###################################################################################################################
#FUNÇÃO SIMPLEX COMEÇA A EXCECUTAR AQUI!
entradas(m,n)
A = np.array(A)
b = np.array(b)
c = np.array(c)

fxblist = []

x = fase1(A,m,n,b)
vb = x[0]
vn = x[1]
fxblist = []
x = metodo(A,vb,vn,c,b)

print(f'A solução ótima é dada em: {x[1]}')
print(f'O valor ótimo é f(xb) = {x[0]}')