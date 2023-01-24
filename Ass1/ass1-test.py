#import the necessary functions from library
from random import shuffle 
from copy import deepcopy   
from collections import defaultdict
from time import perf_counter as stopwatch

#hash function converts the 3d list to a string for use in defaultdict
def hash(arr):
    a = ''
    for i in arr:
        for j in i:
            a += str(j)
    return a

#prints the board
def printBoard(arr):
    for i in arr:
        for j in i:
            print("B", end=" ") if j == 0 else print(j, end=" ")
        print('\n')

#if possible to move the blank up, moves it and returns the result.
#if no move is possible returns a blank list
def moveUp(currentBoard, i, j):
    arr = deepcopy(currentBoard)
    if(i - 1 >= 0):
        arr[i - 1][j], arr[i][j] = arr[i][j], arr[i - 1][j]
        return arr
    return []

#if possible to move the blank down, moves it and returns the result.
#if no move is possible returns a blank list
def moveDown(currentBoard, i, j):
    arr = deepcopy(currentBoard)
    if(i + 1 < 3):
        arr[i + 1][j], arr[i][j] = arr[i][j], arr[i + 1][j]
        return arr
    return []

#if possible to move the blank left, moves it and returns the result.
#if no move is possible returns a blank list
def moveLeft(currentBoard, i, j):
    arr = deepcopy(currentBoard)
    if(j - 1 >= 0):
        arr[i][j - 1], arr[i][j] = arr[i][j], arr[i][j - 1]
        return arr
    return []

#if possible to move the blank result, moves it and returns the result.
#if no move is possible returns a blank list
def moveRight(currentBoard, i, j):
    arr = deepcopy(currentBoard)
    if(j + 1 < 3):
        arr[i][j + 1], arr[i][j] = arr[i][j], arr[i][j + 1]
        return arr
    return []

#given a input state, returns the possible state that could be reached. 
def getPossibleStates(currentBoard):
    i = 0
    j = 0
    for k in range(9):  #searches for the index of zero
        if not (currentBoard[k//3][k%3]):
            i = k // 3
            j = k % 3

    possibleStates = [] #stores the state that could be reached
    a1 = moveDown(currentBoard, i, j)
    a2 = moveLeft(currentBoard, i, j)
    a3 = moveRight(currentBoard, i, j)
    a4 = moveUp(currentBoard, i, j)

    if(len(a1)):
        possibleStates.append(a1)
    if(len(a2)):
        possibleStates.append(a2)
    if(len(a3)):
        possibleStates.append(a3)
    if(len(a4)):
        possibleStates.append(a4)
    return possibleStates    

#Given the initial board, searches for the end state using BFS
def bfs(initial, final):
    #print("Using BFS to solve for- ")
    #printBoard(initial)
    _bfs = 0
    queue = []
    statesTaken = defaultdict(lambda: False) #a map for checking which states were reached, returns false by default 
    queue.append(initial)
    m = initial
    while queue:
        m = queue.pop(0)
        if statesTaken[hash(m)]:
            continue
        _bfs += 1
        statesTaken[hash(m)] = True
        #print(f"BFS has checked: {_bfs} states", end='\r')
        if m == final:
            #print(f"\nFinal State Reached\n in {_bfs} steps.")
            #printBoard(m)
            break;
        for neighbour in getPossibleStates(m):
            if not statesTaken[hash(neighbour)]:
                queue.append(neighbour)
    return _bfs, m

#Given the initial board, searches for the end state using BFS
def dfs(initial, final):
    #print("Using DFS to solve for- ")
    #printBoard(initial)
    _dfs = 0
    queue = []
    statesTaken = defaultdict(lambda: False) #a map for checking which states were reached, returns false by default 
    queue.append(initial)
    m = initial
    while queue:
        m = queue.pop()
        if statesTaken[hash(m)]:
            continue
        statesTaken[hash(m)] = True
        _dfs += 1
        #print(f"DFS has checked: {_dfs} states", end='\r')
        if m == final:
            #print(f"\nFinal State Reached in {_dfs} steps\n")
            #printBoard(m)
            break;
        for neighbour in getPossibleStates(m):
            if not statesTaken[hash(neighbour)]:
                queue.append(neighbour)
    return _dfs, m

#auxillary function calls the main bfs function and also prints useful info.
def auxBFS(initial, final):
    _bfs, ans = bfs(initial, final)

#auxillary function calls the main dfs function and also prints useful info.
def auxDFS(initial, final):
    _dfs, ans = dfs(initial, final)

if __name__ == '__main__':
    final_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]   #desired final state as a 2d array

    final = []  #converts a 9dim 1d array to a 3x3 2d array
    for i in range(3):
        arr = []
        for j in range(3):
            arr.append(final_state[3 * i + j])
        final.append(arr)

    #print("Randomly generated initial board.\n")

    '''
    3 arrays are stored that were used for checking the correctness of the algo,
    they can be uncommented for use

    deepState = [[4, 8, 2], [0, 1, 5], [3, 7, 6]]
    shallowState = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
    impossibleState = [[1,2,3], [4,5,6], [8,7,0]]
    '''

    bfs_win = 0
    dfs_win = 0
    bfs_time = 0
    dfs_time = 0
    for i in range(50):
        print(f'{i+1}/50', end='\r')
        initial_state = list(range(9))
        shuffle(initial_state)
        initial = []    #converts a 9dim 1d array to a 3x3 2d array
        for i in range(3):
            arr = []
            for j in range(3):
                arr.append(initial_state[3 * i + j])
            initial.append(arr)

        startBFS = stopwatch()
        auxBFS(initial, final)
        endBFS = stopwatch()

        startDFS = stopwatch()
        auxDFS(initial, final)
        endDFS = stopwatch()

        bTime = endBFS - startBFS
        dTime = endDFS - startDFS
        bfs_time += bTime
        dfs_time += dTime

        if(bTime < dTime):
            bfs_win += 1
        elif(dTime < bTime):
            dfs_win += 1

    print(f"Average time BFS: {bfs_time / 50}")
    print(f"Average time DFS: {dfs_time / 50}")
    print(f'\nBFS wins: {bfs_win}')
    print(f'\nDFS wins: {dfs_win}')
