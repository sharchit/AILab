from random import randint
N = 8

def configureRandomly(board, row_of_queen):
    for i in range(N):
        row_of_queen[i] = randint(0, N-1)
        board[row_of_queen[i]][i] = 1

def printBoard(board):
    print('\n\n')
    for i in board:
        print(i)
    
def compareState(row_of_queen1, row_of_queen2):
    for i in range(N):
        if (row_of_queen1[i] != row_of_queen2[i]):
            return False
    return True

def fill(board, value):
    for i in range(N):
        for j in range(N):
            board[i][j] = value
        
def pairsAttacking( board, row_of_queen):
    attacking = 0
    for i in range(N):
        # check left side on row
        row = row_of_queen[i]
        col = i - 1
        while (col >= 0 and board[row][col] != 1) :
            col -= 1
        if (col >= 0 and board[row][col] == 1) :
            attacking += 1

        # check right side on row
        row = row_of_queen[i]
        col = i + 1
        while (col < N and board[row][col] != 1):
            col += 1
        if (col < N and board[row][col] == 1) :
            attacking += 1
        row = row_of_queen[i] - 1
        col = i - 1

        # check top left diagonal
        while (col >= 0 and row >= 0 and board[row][col] != 1) :
            col-= 1
            row-= 1
        if (col >= 0 and row >= 0 and board[row][col] == 1) :
            attacking+= 1
        row = row_of_queen[i] + 1
        col = i + 1

        # check bottom right diagonal 
        while (col < N and row < N and board[row][col] != 1) :
            col+= 1
            row+= 1
        if (col < N and row < N and board[row][col] == 1) :
            attacking += 1
        row = row_of_queen[i] + 1
        col = i - 1

        # check bottlom left diagonal
        while (col >= 0 and row < N and board[row][col] != 1) :
            col -= 1
            row += 1
        if (col >= 0 and row < N and board[row][col] == 1) :
            attacking += 1
        row = row_of_queen[i] - 1
        col = i + 1

        # check top right diagonal
        while (col < N and row >= 0 and board[row][col] != 1) :
            col += 1
            row -= 1
        if (col < N and row >= 0 and board[row][col] == 1) :
            attacking += 1
    return attacking // 2

def generateBoard( board, row_of_queen):
    fill(board, 0)
    for i in range(N):
        board[row_of_queen[i]][i] = 1
def copyrow_of_queen( row_of_queen1, row_of_queen2):
    for i in range(N):
        row_of_queen1[i] = row_of_queen2[i]
def getNeighbour(board, row_of_queen):
    opBoard = [[0 for _ in range(N)] for _ in range(N)]
    oprow_of_queen = [0 for _ in range(N)]
    copyrow_of_queen(oprow_of_queen, row_of_queen)
    generateBoard(opBoard, oprow_of_queen)
    opObjective = pairsAttacking(opBoard, oprow_of_queen)
    NeighbourBoard = [[0 for _ in range(N)] for _ in range(N)]
    
    Neighbour_row_of_queen = [0 for _ in range(N)]
    copyrow_of_queen(Neighbour_row_of_queen, row_of_queen)
    generateBoard(NeighbourBoard, Neighbour_row_of_queen)
    for i in range(N):
        for j in range(N):
            if (j != row_of_queen[i]) :
                Neighbour_row_of_queen[i] = j
                NeighbourBoard[Neighbour_row_of_queen[i]][i] = 1
                NeighbourBoard[row_of_queen[i]][i] = 0
                temp = pairsAttacking( NeighbourBoard, Neighbour_row_of_queen)
                if (temp <= opObjective) :
                    opObjective = temp
                    copyrow_of_queen(oprow_of_queen, Neighbour_row_of_queen)
                    generateBoard(opBoard, oprow_of_queen)
                NeighbourBoard[Neighbour_row_of_queen[i]][i] = 0
                Neighbour_row_of_queen[i] = row_of_queen[i]
                NeighbourBoard[row_of_queen[i]][i] = 1
    copyrow_of_queen(row_of_queen, oprow_of_queen)
    fill(board, 0)
    generateBoard(board, row_of_queen)
def hillClimbing(board, row_of_queen):
    neighbourBoard = [[0 for _ in range(N)] for _ in range(N)]
    Neighbour_row_of_queen = [0 for _ in range(N)]
    copyrow_of_queen(Neighbour_row_of_queen, row_of_queen)
    generateBoard(neighbourBoard, Neighbour_row_of_queen)
    i = 0
    while True:
        copyrow_of_queen(row_of_queen, Neighbour_row_of_queen)
        generateBoard(board, row_of_queen)
        getNeighbour(neighbourBoard, Neighbour_row_of_queen)
        if (compareState(row_of_queen, Neighbour_row_of_queen)) :
            printBoard(board)
            break
        
        elif (pairsAttacking(board, row_of_queen) == pairsAttacking( neighbourBoard,Neighbour_row_of_queen)):
            Neighbour_row_of_queen[randint(0, N-1)] = randint(0, N-1)
            generateBoard(neighbourBoard, Neighbour_row_of_queen)
        
        i += 1
        print(f"\rStates checked: {i}", end="")


# row_of_queen = [0] * N
# board = [[0 for _ in range(N)] for _ in range(N)]
# configureRandomly(board, row_of_queen)
# hillClimbing(board, row_of_queen)

if __name__ == '__main__':
    N = int(input("Enter the value of N: "))
    row_of_queen = [0] * N
    board = [[0]*N for _ in range(N)]

    print(f"Enter the row and column of the {N} starting positions of queen: ")
    for _ in range(N):
        x, y = list(map(int, input().split()))
        board[x][y] = 1

    printBoard(board)

    for _ in range(3):
        configureRandomly(board, row_of_queen)
        hillClimbing(board, row_of_queen)