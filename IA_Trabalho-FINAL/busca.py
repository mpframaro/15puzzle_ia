import copy
import numpy as np
import sys 
import time
class Board():#para criar cada estado
    def __init__(self,matrix,moves,cost,pos):
        self.matrix = matrix
        self.moves = moves
        self.cost = cost
        self.pos = pos

def moveUp(matrix,pos): #pos é a coordenada da celula vazia
    matriz = copy.deepcopy(matrix)
    row = pos[0]
    col = pos[1]
    if row == 0:
        return 
    else:
         matriz[row][col] , matriz[row-1][col] = matriz[row-1][col] , 0
    return matriz

def moveDown(matrix,pos): #pos é a coordenada da celula vazia
    matriz = copy.deepcopy(matrix)
    row = pos[0]
    col = pos[1]
    if row == 3:
        return 
    else:
         matriz[row][col] , matriz[row+1][col] = matriz[row+1][col] , 0
    return matriz

def moveRight(matrix,pos): #pos é a coordenada da celula vazia
    matriz = copy.deepcopy(matrix)
    row = pos[0]
    col = pos[1]
    if col == 3:
        return 
    else:
         matriz[row][col] , matriz[row][col+1] = matriz[row][col+1] , 0
    return matriz

def moveLeft(matrix,pos): #pos é a coordenada da celula vazia
    matriz = copy.deepcopy(matrix)
    row = pos[0]
    col = pos[1]
    if col == 0:
        return 
    else:
         matriz[row][col] , matriz[row][col-1] = matriz[row][col-1] , 0
    return matriz

def makeallmoves(board):
    movimentos = []
    moves = board.moves
    pos = board.pos
    movimentos.append(Board(moveUp(board.matrix,pos),moves + ["up"],board.cost+1,[pos[0]-1,pos[1]]))
    movimentos.append(Board(moveDown(board.matrix,pos),moves + ["down"],board.cost+1,[pos[0]+1,pos[1]]))
    movimentos.append(Board(moveRight(board.matrix,pos),moves + ["right"],board.cost+1,[pos[0],pos[1]+1]))
    movimentos.append(Board(moveLeft(board.matrix,pos),moves + ["left"],board.cost+1,[pos[0],pos[1]-1]))
    movi = [b for b in movimentos if b.matrix is not None]
    return movi

def createMatrix(config):
    matrix = np.zeros((4,4))
    j =0
    for i in range(4): #converter lista de ints em matriz para mais fácil resolução
        for d in range(4):
            matrix[i][d] = config[j]
            j+= 1
    return matrix

def inversions(config): 
    counter = 0
    for i in range(16):
        for j in range(16):
            if config[j] < config[i] and i < j and  config[j] != 0:
                counter += 1
    return counter

def blankRow(config):
    matrix = createMatrix(config)
    for i in range(4):
        for j in range(4):
            if matrix[i][j] == 0:
                return 4 - i

def solvable(config):
    if (inversions(config) % 2 == 0) == (blankRow(config) %2 == 1):
        return True
    return False

def thereIsNoSolution(configInicial,configFinal):
    if solvable(configInicial) == solvable(configFinal):
        return False
    return True

def bfs(configInicial,configFinal): #pesquisa em largura
    matrixi = createMatrix(configInicial)
    matrixfin = createMatrix(configFinal)
    poss =[0,0]
    poss[0] = (configInicial.index(0))//4
    poss[1] = configInicial.index(0)%4 
    queue = list()
    visited = set()
    queue.append(Board(matrixi,[],0,poss))
    max = 0
    i = 0
    while len(queue) >0:
        d = queue[i]
        if len(queue)> max :
            max = len(queue)
        if np.array_equal(d.matrix,matrixfin):
            print('Numero maximo de nos guardados: ' + str(max))
            return d.moves
        else:
            descended = makeallmoves(d)
            for state in descended:
                if (hash(str(state.matrix)) not in visited):
                    queue.append(state)
                    visited.add(hash(str(state.matrix)))
        i =i+1
    
def dfs(configInicial,configFinal): #pesquisa em profundidade
    matrixi = createMatrix(configInicial)
    matrixfin = createMatrix(configFinal)
    poss =[0,0]
    poss[0] = (configInicial.index(0))//4
    poss[1] = configInicial.index(0)%4 
    queue = list()
    visited = set()
    queue.append(Board(matrixi,[],0,poss))
    max =0
    while len(queue) >0:
        if len(queue)> max :
            max = len(queue)
        d = queue.pop(0)
        if np.array_equal(d.matrix,matrixfin):#completar depois
            print('numero maximo de nos guardados: ' + str(max))
            return d.moves
        else:
            descended = makeallmoves(d)
            for state in descended:
                nos = list()
                if hash(str(state.matrix)) not in visited:
                    visited.add(hash(str(state.matrix)))
                    nos.append(state)
                queue = nos + queue
    return None

def idfs(configInicial,configFinal): #iterativa em profundidade
    matrixi = createMatrix(configInicial)
    matrixfin = createMatrix(configFinal)
    poss =[0,0]
    poss[0] = (configInicial.index(0))//4
    poss[1] = configInicial.index(0)%4 
    maxmoves = 2
    while True:
        queue = list()
        queue.append(Board(matrixi,[],0,poss))
        max =0
        while len(queue) >0:
            if len(queue)> max :
                max = len(queue)
            d = queue.pop(0)
            if not (len(d.moves) > maxmoves):
                if np.array_equal(d.matrix,matrixfin):
                    print('Numero maximo de nos guardados: ' + str(max))
                    return d.moves
                else:
                    descended = makeallmoves(d)
                    for state in descended:
                        nos = list()
                        nos.append(state)
                        queue = nos + queue
        maxmoves +=1

def aesterick(configInicial,configFinal,heuri): #A*
    matrixi = createMatrix(configInicial)
    matrixfin = createMatrix(configFinal)
    poss =[0,0]
    poss[0] = (configInicial.index(0))//4
    poss[1] = configInicial.index(0)%4
    boardini = Board(matrixi,[],0,poss)
    openlist = list()
    f =heuristic(boardini,matrixfin,heuri) + boardini.cost
    openlist.append((f,boardini))
    max = 1
    while len(openlist)>0:
        if len(openlist)> max :
            max = len(openlist)
        p = openlist.pop(0)
        f =p[0]
        d =p[1]
        if np.array_equal(d.matrix,matrixfin):
            print('Numero maximo de nos guardados: ' + str(max))
            return d.moves
        else:
            descended = makeallmoves(d)
            for child in descended:
                fc = heuristic(child,matrixfin,heuri) + child.cost
                openlist.append((fc,child))
        openlist.sort(key = lambda x: x[0])

def heuristic(board,goal,heuri):# 1-numero de pecas fora de lugar 2- manhanthan distance
    matri = board.matrix
    counter = 0
    if heuri == 1:
        for i in range(4):
            for j in range(4):
                if matri[i][j] != goal[i][j]:
                    counter += 1
        return counter 
    else:
        for i in range(4):
            for j in range(4):
                k =0
                l=0
                n = 0
                if matri[i][j] != goal[i][j]:
                    while matri[i][j] != goal[k][l]:
                        n = n +1
                        l = n %4
                        k = n // 4
                    counter = counter + abs(k-i) +abs(l-j) 
        return counter 

def greedy(configInicial,configFinal,heuri):#pesquisa golosa
    matrixi = createMatrix(configInicial)
    matrixfin = createMatrix(configFinal)
    poss =[0,0]
    poss[0] = (configInicial.index(0))//4
    poss[1] = configInicial.index(0)%4
    boardini = Board(matrixi,[],0,poss)
    openlist = list()
    closed = set()
    f =heuristic(boardini,matrixfin,heuri)
    openlist.append((f,boardini))
    max =0
    while len(openlist)>0:
        if len(openlist)> max :
            max = len(openlist)
        p = openlist.pop(0)
        f =p[0]
        d =p[1]
        if np.array_equal(d.matrix,matrixfin):
            print('Numero maximo de nos guardados: ' + str(max))
            return d.moves
        else:
            descended = makeallmoves(d)
            for child in descended:
                if hash(str(child.matrix)) not in closed:
                    fc = heuristic(child,matrixfin,heuri)
                    openlist.append((fc,child))
                    closed.add(hash(str(child.matrix)))
        openlist.sort(key = lambda x: x[0])
    return None

def buscaUtilizar(s):
    modos=["DFS", "BFS", "IDFS", "A*-misplaced", "A*-Manhattan","Greedy-misplaced", "Greedy-Manhattan"]
    for i in range(len(modos)):
        if s == modos[i]:
            return i
    return -1
        
def busca(confinginicial,configfinal,modo):
    if modo == 0:
        return dfs(confinginicial,configfinal)
    elif modo == 1:
        return bfs(confinginicial,configfinal)
    elif modo == 2:
        return idfs(confinginicial,configfinal)
    elif modo == 3:
        return aesterick(confinginicial,configfinal,1)
    elif modo == 4:
        return aesterick(confinginicial,configfinal,2)
    elif modo == 5:
        return greedy(confinginicial,configfinal,1)
    else :
        return greedy(confinginicial,configfinal,2)

s = sys.argv[1]
inicial = list(map(int, input().split()))
final = list(map(int, input().split()))
epoch = time.time()

if not thereIsNoSolution(inicial,final):
    algoritmo = buscaUtilizar(s)
    if algoritmo >= 0:
        resposta = busca(inicial,final,algoritmo)
        time_sec = time.time()
        print("Duracao do algoritmo em segundos:", time_sec-epoch)
        if resposta == None:
            print('Solucao nao foi encontrada')
        else:
            print('Numero de jogadas necessarias:',len(resposta))
            print('Jogadas:',resposta)
    else:
        print('O algoritmo escolhido nao e uma das opcoes')
else:
    print('Nao tem solucao')
