#import the necessary functions from library
from random import shuffle 
from copy import deepcopy   
from collections import defaultdict
from time import perf_counter as stopwatch
from queue import PriorityQueue
import math

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
    for x in range(1,9):
        for i in range(3):
            for j in range(3):
                if(initial[i][j] == x):
                    start_x = i
                    start_y = j
                if(neighbour[i][j] == x):
                    last_x = i
                    last_y = j
        manhattan += abs(last_x - start_x) + abs(last_y - start_y)
    return manhattan

def h4(neighbour):
    return 0.5*h2(neighbour) + 0.5*h3(neighbour)

def h5(neighbour):
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
    return manhattan

def aStar_with_h1(initial, final):
    print("Using aStar w/ h1 to solve for- ")
    print(initial)
    distance = defaultdict(lambda: math.inf)
    parent = defaultdict(lambda: None)
    distance[hash(initial)] = 0
    queue = PriorityQueue()
    queue.put((distance[hash(initial)], initial))
    _aStar = 0
    verify = []
    arr = set()
    while not queue.empty():
        dist, m = queue.get()
        _aStar += 1
        for neighbour in getPossibleStates(m):
            tempDistance = dist + 1 + h1(neighbour)
            if(tempDistance < distance[hash(neighbour)]):
                distance[hash(neighbour)] = tempDistance
                parent[hash(neighbour)] = m
                queue.put((distance[hash(neighbour)], neighbour))
                arr.add(hash(neighbour))
                if h1(neighbour) + dist + 1 >= h1(m):
                    verify.append(True)
                else:
                    verify.append(False)
        if(m == final):
            break
    print(f"aStar has checked: {_aStar} states")
    if(distance[hash(final)] != math.inf):
        print(f'Final state reached.\nOptimal path is {distance[hash(final)]}.')
        print(final)
        print('The path will be- ')
        current = final
        while(parent[hash(current)] != None):
            print(current)
            current = parent[hash(current)]
        print(initial)
    else:
        print(f'Final state not reachable.')
    print(f'Monotonicity verification: {all(verify)}')
    return arr

def aStar_with_h2(initial, final):
    print("Using aStar w/ h2 to solve for- ")
    print(initial)
    distance = defaultdict(lambda: math.inf)
    parent = defaultdict(lambda: None)
    cost = defaultdict(lambda: math.inf)
    distance[hash(initial)] = 0
    queue = PriorityQueue()
    queue.put((distance[hash(initial)], initial))
    _aStar = 0
    verify = []
    while not queue.empty():
        dist, m = queue.get()
        _aStar += 1
        for neighbour in getPossibleStates(m):
            tempDistance = dist + 1 + h2(neighbour)
            if(tempDistance < distance[hash(neighbour)]):
                distance[hash(neighbour)] = tempDistance
                cost[hash(neighbour)] = dist + 1
                parent[hash(neighbour)] = m
                queue.put((distance[hash(neighbour)], neighbour))
                if h2(neighbour) + cost[hash(neighbour)]>= h2(m):
                    verify.append(True)
                else:
                    verify.append(False)
        if(m == final):
            break
    print(f"aStar has checked: {_aStar} states")
    if(distance[hash(final)] != math.inf):
        print(f'Final state reached.\nOptimal path is {distance[hash(final)]}.')
        print(final)
        print('The path will be- ')
        current = final
        while(parent[hash(current)] != None):
            print(current)
            current = parent[hash(current)]
        print(initial)
    else:
        print(f'Final state not reachable.')
    print(f'Monotonicity verification: {all(verify)}')
    

def aStar_with_h3(initial, final):
    print("Using aStar w/ h3 to solve for- ")
    print(initial)
    distance = defaultdict(lambda: math.inf)
    parent = defaultdict(lambda: None)
    cost = defaultdict(lambda: math.inf)
    distance[hash(initial)] = 0
    queue = PriorityQueue()
    queue.put((distance[hash(initial)], initial))
    _aStar = 0
    verify = []
    arr = set()
    while not queue.empty():
        dist, m = queue.get()
        _aStar += 1
        for neighbour in getPossibleStates(m):
            tempDistance = dist + 1 + h3(neighbour)
            if(tempDistance < distance[hash(neighbour)]):
                distance[hash(neighbour)] = tempDistance
                parent[hash(neighbour)] = m
                cost[hash(neighbour)] = dist + 1
                arr.add(hash(neighbour))
                queue.put((distance[hash(neighbour)], neighbour))
                if h3(neighbour) + cost[hash(neighbour)] >= h3(m):
                    verify.append(True)
                else:
                    verify.append(False)
        if(m == final):
            break
    print(f"aStar has checked: {_aStar} states")
    if(distance[hash(final)] != math.inf):
        print(f'Final state reached.\nOptimal path is {distance[hash(final)]}.')
        print(final)
        print('The path will be- ')
        current = final
        while(parent[hash(current)] != None):
            print(current)
            current = parent[hash(current)]
        print(initial)
    else:
        print(f'Final state not reachable.')
    print(f'Monotonicity verification: {all(verify)}')
    return arr

def aStar_with_h4(initial, final):
    print("Using aStar w/ h4 to solve for- ")
    print(initial)
    distance = defaultdict(lambda: math.inf)
    parent = defaultdict(lambda: None)
    distance[hash(initial)] = 0
    queue = PriorityQueue()
    queue.put((distance[hash(initial)], initial))
    cost = defaultdict(lambda: math.inf)
    _aStar = 0
    verify =[]
    while not queue.empty():
        dist, m = queue.get()
        _aStar += 1
        for neighbour in getPossibleStates(m):
            tempDistance = dist + 1 + h4(neighbour)
            if(tempDistance < distance[hash(neighbour)]):
                distance[hash(neighbour)] = tempDistance
                parent[hash(neighbour)] = m
                cost[hash(neighbour)] = dist + 1
                queue.put((distance[hash(neighbour)], neighbour))
                if h4(neighbour) + cost[hash(neighbour)] >= h4(m):
                    verify.append(True)
                else:
                    verify.append(False)
        if(m == final):
            break
    print(f"aStar has checked: {_aStar} states")
    if(distance[hash(final)] != math.inf):
        print(f'Final state reached.\nOptimal path is {distance[hash(final)]}.')
        print(final)
        print('The path will be- ')
        current = final
        while(parent[hash(current)] != None):
            print(current)
            current = parent[hash(current)]
        print(initial)
    else:
        print(f'Final state not reachable.')
    print(f'Monotonicity verification: {all(verify)}')

def aStar_with_h5(initial, final):
    print("Using aStar w/ h5 to solve for- ")
    print(initial)
    distance = defaultdict(lambda: math.inf)
    parent = defaultdict(lambda: None)
    distance[hash(initial)] = 0
    queue = PriorityQueue()
    queue.put((distance[hash(initial)], initial))
    cost = defaultdict(lambda: math.inf)
    _aStar = 0
    verify =[]
    while not queue.empty():
        dist, m = queue.get()
        _aStar += 1
        for neighbour in getPossibleStates(m):
            tempDistance = dist + 1 + h5(neighbour)
            if(tempDistance < distance[hash(neighbour)]):
                distance[hash(neighbour)] = tempDistance
                parent[hash(neighbour)] = m
                cost[hash(neighbour)] = dist + 1
                queue.put((distance[hash(neighbour)], neighbour))
                if h5(neighbour) + cost[hash(neighbour)] >= h5(m):
                    verify.append(True)
                else:
                    verify.append(False)
        if(m == final):
            break
    print(f"aStar has checked: {_aStar} states")
    if(distance[hash(final)] != math.inf):
        print(f'Final state reached.\nOptimal path is {distance[hash(final)]}.')
        print(final)
        print('The path will be- ')
        current = final
        while(parent[hash(current)] != None):
            print(current)
            current = parent[hash(current)]
        print(initial)
    else:
        print(f'Final state not reachable.')
    print(f'Monotonicity verification: {all(verify)}')

def isSolvable(arr):
    inv = 0
    arr = hash(arr)
    empty_value = '0'
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if arr[j] != empty_value and arr[i] != empty_value and int(arr[i]) > int(arr[j]):
                inv += 1
    if inv % 2 == 0:
        print(f'Solvable')
    else:
        print(f'Unsolvable')

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
    source = [[2, 3, 4], [1, 5, 6], [8, 7, 0]]
    
    t1 = stopwatch()
    s1 = aStar_with_h1(source, final)
    t2 = stopwatch()
    print(f"AStar with h1 took {round(t2-t1, 3)}s\n\n")
    
    t1 = stopwatch()
    aStar_with_h2(source, final)
    t2 = stopwatch()
    print(f"AStar with h2 took {round(t2-t1, 3)}s\n\n")

    t1 = stopwatch()
    s2 = aStar_with_h3(source, final)
    t2 = stopwatch()
    print(f"AStar with h3 took {round(t2-t1, 3)}s\n\n")

    t1 = stopwatch()
    aStar_with_h4(source, final)
    t2 = stopwatch()
    print(f"AStar with h4 took {round(t2-t1, 3)}s\n\n")

    t1 = stopwatch()
    aStar_with_h5(source, final)
    t2 = stopwatch()
    print(f"AStar with h5 took {round(t2-t1, 3)}s\n\n")


    print(f'Superset: {s1.issuperset(s2)}')
    solve=[[[4, 8, 2], [0, 1, 5], [3, 7, 6]], [[4, 0, 8], [2, 7, 5], [1, 3, 6]], [[6, 7, 3], [1, 0, 2], [4, 8, 5]], [[5, 4, 8], [6, 0, 1], [2, 7, 3]], 
    [[8, 4, 1], [0, 7, 6], [2, 5, 3]], [[2, 7, 3], [5, 4, 1], [6, 8, 0]], [[2, 5, 1], [4, 6, 7], [0, 8, 3]], [[2, 3, 4], [1, 5, 6], [8, 7, 0]], [[2, 3, 4], [1, 5, 6], [8, 7, 0]],
    [[2, 6, 8], [1, 7, 0], [5, 4, 3]]]


    for q in solve:
        isSolvable(q)