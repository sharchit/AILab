#import the necessary functions from library
from random import shuffle 
from copy import deepcopy   
from collections import defaultdict
from time import perf_counter as stopwatch
from queue import PriorityQueue

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

def h1(neighbour):
    return 0

def h2(neighbour):
    initial = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    _displaced = 0
    for i in range(3):
        for j in range(3):
            if(initial[i][j] != neighbour[i][j]):
                _displaced += 1
    return _displaced

def h3(neighbour):
    initial = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    start_x = 0
    start_y = 0
    last_x = 0
    last_y = 0
    manhattan = 0
    for x in range(9):
        for i in range(3):
            for j in range(3):
                if(initial[i][j] == x):
                    start_x = i
                    start_y = j
                if(neighbour[i][j] == x):
                    last_x = i
                    last_y = j
        manhattan += abs(last_x - start_x) + abs(last_y - start_y)
    return deepState

def h4(neighbour):
    return 0.5*h2(neighbour) + 0.5*h3(neighbour)

def aStar_with_h1(initial, final):
    print("Using aStar w/ h3 to solve for- ")
    printBoard(initial)
    _aStar = 0
    _level = 0
    queue = PriorityQueue()
    statesTaken = defaultdict(lambda: False) #a map for checking which states were reached, returns false by default 
    queue.put((0, initial))
    m = initial
    while not queue.empty():
        m = queue.get()[1]
        if statesTaken[hash(m)]:
            continue
        _aStar += 1
        statesTaken[hash(m)] = True
        print(f"aStar with h3 has checked: {_aStar} states", end='\r')
        if m == final:
            print(f"\nFinal State Reached in {_aStar} steps.")
            printBoard(m)
            break
        for neighbour in getPossibleStates(m):
            if not statesTaken[hash(neighbour)]:
                queue.put((h1(neighbour)+_level, neighbour))
    return _aStar, m, _level

def aStar_with_h2(initial, final):
    print("Using aStar w/ h2 to solve for- ")
    printBoard(initial)
    _aStar = 0
    _level = 0
    queue = PriorityQueue()
    statesTaken = defaultdict(lambda: False) #a map for checking which states were reached, returns false by default 
    queue.put((0, initial))
    m = initial
    while not queue.empty():
        m = queue.get()[1]
        if statesTaken[hash(m)]:
            continue
        _aStar += 1
        statesTaken[hash(m)] = True
        print(f"aStar with h2 has checked: {_aStar} states", end='\r')
        if m == final:
            print(f"\nFinal State Reached in {_aStar} steps.")
            printBoard(m)
            break
        _level += 1
        for neighbour in getPossibleStates(m):
            if not statesTaken[hash(neighbour)]:
                queue.put((h2(neighbour)+_level, neighbour))
    return _aStar, m, _level

def aStar_with_h3(initial, final):
    print("Using aStar w/ h1 to solve for- ")
    printBoard(initial)
    _aStar = 0
    _level = 0
    queue = PriorityQueue()
    statesTaken = defaultdict(lambda: False) #a map for checking which states were reached, returns false by default 
    queue.put((0, initial))
    m = initial
    while not queue.empty():
        m = queue.get()[1]
        if statesTaken[hash(m)]:
            continue
        _aStar += 1
        statesTaken[hash(m)] = True
        print(f"aStar w/ h1 has checked: {_aStar} states", end='\r')
        if m == final:
            print(f"\nFinal State Reached in {_aStar} steps.")
            printBoard(m)
            break
        _level += 1
        for neighbour in getPossibleStates(m):
            if not statesTaken[hash(neighbour)]:
                queue.put((h3(neighbour)+_level, neighbour))
    return _aStar, m, _level

def aStar_with_h4(initial, final):
    print("Using aStar w/ h4 to solve for- ")
    printBoard(initial)
    _aStar = 0
    _level = 0
    queue = PriorityQueue()
    statesTaken = defaultdict(lambda: False) #a map for checking which states were reached, returns false by default 
    queue.put((0, initial))
    m = initial
    while not queue.empty():
        m = queue.get()[1]
        if statesTaken[hash(m)]:
            continue
        _aStar += 1
        statesTaken[hash(m)] = True
        print(f"aStar w/ h4 has checked: {_aStar} states", end='\r')
        if m == final:
            print(f"\nFinal State Reached in {_aStar} steps.")
            printBoard(m)
            break
        _level += 1
        for neighbour in getPossibleStates(m):
            if not statesTaken[hash(neighbour)]:
                queue.put((h4(neighbour)+_level, neighbour))
    return _aStar, m, _level

#auxillary functions calls the main functions and also prints useful info.
def aux_h1(initial, final):
    statesChecked, finalBoard, optimalCost = aStar_with_h1(initial, final)
    if finalBoard == final:
        print(f"aStar w/ h3 checked {statesChecked} states to reach the final state. i.e.")
        printBoard(finalBoard)
        #print(f"Optimal path Cost is {optimalCost}")
    else:
        print(f"Not possible to reach the final state by aStar. {statesChecked} states checked.")
    return optimalCost

def aux_h2(initial, final):
    statesChecked, finalBoard, optimalCost = aStar_with_h2(initial, final)
    if finalBoard == final:
        print(f"aStar w/ h2 checked {statesChecked} states to reach the final state. i.e.")
        printBoard(finalBoard)
        #print(f"Optimal path Cost is {optimalCost}")
    else:
        print(f"Not possible to reach the final state by aStar. {statesChecked} states checked.")
    return 

def aux_h3(initial, final):
    statesChecked, finalBoard, optimalCost = aStar_with_h3(initial, final)
    if finalBoard == final:
        print(f"aStar w/ h1 checked {statesChecked} states to reach the final state. i.e.")
        printBoard(finalBoard)
        #print(f"Optimal path Cost is {optimalCost}")
    else:
        print(f"Not possible to reach the final state by aStar. {statesChecked} states checked.")

def aux_h4(initial, final):
    statesChecked, finalBoard, optimalCost = aStar_with_h4(initial, final)
    if finalBoard == final:
        print(f"aStar w/ h4 checked {statesChecked} states to reach the final state. i.e.")
        printBoard(finalBoard)
        #print(f"Optimal path Cost is {optimalCost}")
    else:
        print(f"Not possible to reach the final state by aStar. {statesChecked} states checked.")

if __name__ == '__main__':
    final_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]   #desired final state as a 2d array
    initial_state = list(range(9))
    shuffle(initial_state)  #randomly generated initial state

    final = []  #converts a 9dim 1d array to a 3x3 2d array
    for i in range(3):
        arr = []
        for j in range(3):
            arr.append(final_state[3 * i + j])
        final.append(arr)

    initial = []    #converts a 9dim 1d array to a 3x3 2d array
    for i in range(3):
        arr = []
        for j in range(3):
            arr.append(initial_state[3 * i + j])
        initial.append(arr)

    print("Randomly generated initial board.\n")

    '''
    3 arrays are stored that were used for checking the correctness of the algo,
    they can be uncommented for use

    deepState = [[4, 8, 2], [0, 1, 5], [3, 7, 6]]
    shallowState = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
    impossibleState = [[1,2,3], [4,5,6], [8,7,0]]
    '''
    deepState = [[4, 8, 2], [0, 1, 5], [3, 7, 6]]
    shallowState = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
    impossibleState = [[1,2,3], [4,5,6], [8,7,0]]
    source = [[1,2,3],[0,4,6],[7,5,8]]
    t1 = stopwatch()
    aux_h3(deepState, final)
    t2 = stopwatch()
    print(f"AStar with h1 took {round(t2-t1, 3)}s")
    
    t1 = stopwatch()
    aux_h2(deepState, final)
    t2 = stopwatch()
    print(f"AStar with h2 took {round(t2-t1, 3)}s")

    t1 = stopwatch()
    aux_h1(deepState, final)
    t2 = stopwatch()
    print(f"AStar with h3 took {round(t2-t1, 3)}s")

    t1 = stopwatch()
    aux_h4(deepState, final)
    t2 = stopwatch()
    print(f"AStar with h4 took {round(t2-t1, 3)}s")