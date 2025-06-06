#author: Daniel Rossmaier
from tkinter import messagebox
from tkinter import *
import random
import copy 

def is_valid(board, row, col, num):
    # Check row
    if num in board[row]:
        return False
    
    # Check column
    if num in [board[i][col] for i in range(9)]:
        return False

    # Check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False

    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(board)
    return board

def print_sudoku(board):
    for i in range(0,9):
            print(board[i][0],board[i][1],board[i][2],board[i][3],board[i][4],board[i][5],board[i][6],board[i][7],board[i][8],sep=' ')


def sudoku_to_tensor(board_2d):
    tensor = [[[[0 for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for r in range(9):
        for c in range(9):
            br, cr = r // 3, c // 3      # cell row, cell col
            bc, cc = r % 3, c % 3        # big row, big col
            tensor[br][bc][cr][cc] = board_2d[r][c]
    return tensor


def print_field(field):
    for i in range(0,3):
        for j in range(0,3):
            print(field[i][j][0][0],field [i][j][0][1],field[i][j][0][2],
            field[i][j][1][0],field[i][j][1][1],field[i][j][1][2],
            field[i][j][2][0],field[i][j][2][1],field[i][j][2][2],sep=' ')


def rule1_sat(koords):
    #vertical satisfaction
    rule_sat = True
    vertical = []
    for i in range(0,3):
        for j in range(0,3):
            for k in range(0,3):
                for l in range(0,3):
                    if k==koords[2] and l==koords[3]:
                        if not [i,j,k,l]==koords:
                            vertical.append(sfield[i][j][k][l])

    vertical = [number for number in vertical if number > 0]

    if sfield[koords[0]][koords[1]][koords[2]][koords[3]] in vertical:
        #print("vertical")
        #print(koords)
        #print(vertical)
        rule_sat = False

    return rule_sat

def rule2_sat(koords):
    #horizontal satisfaction
    rule_sat = True
    horizontal = []
    for i in range(0,3):
        for j in range(0,3):
            for k in range(0,3):
                for l in range(0,3):
                    if i==koords[0] and j==koords[1]:
                        if not [i,j,k,l]==koords:
                            horizontal.append(sfield[i][j][k][l])

    horizontal = [number for number in horizontal if number > 0]

    if sfield[koords[0]][koords[1]][koords[2]][koords[3]] in horizontal:
        #print("horizontal")
        #print(koords)
        #print(horizontal)
        rule_sat = False

    return rule_sat

def rule3_sat(koords):
    #cluster satisfaction
    rule_sat = True
    cluster = []
    for i in range(0,3):
        for j in range(0,3):
            for k in range(0,3):
                for l in range(0,3):
                    if i==koords[0] and k==koords[2]:
                        if not [i,j,k,l]==koords:
                            cluster.append(sfield[i][j][k][l])

    cluster = [number for number in cluster if number > 0]
    value = sfield[koords[0]][koords[1]][koords[2]][koords[3]]
    if value in cluster:
        #print(value)
        #print("cluster")
        #print(koords)
        #print(cluster)
        rule_sat = False

    return rule_sat


def rule_sat(tensorkoords):
    if rule1_sat(tensorkoords) and rule2_sat(tensorkoords) and rule3_sat(tensorkoords):
        return True
    else:
        return False

def check_sudoku_field():
    for i in range(0,3):
        for j in range(0,3):
            for k in range(0,3):
                for l in range(0,3):
                    if not rule_sat([i,j,k,l]):
                        return False
    return True



def make_puzzle_field(field, clues=30):
    puzzle = copy.deepcopy(field)
    positions = [(br, bc, cr, cc) for br in range(3) for bc in range(3)
                                      for cr in range(3) for cc in range(3)]
    random.shuffle(positions)

    for br, bc, cr, cc in positions:
        removed = puzzle[br][bc][cr][cc]
        puzzle[br][bc][cr][cc] = 0

        if not check_sudoku_field:
            puzzle[br][bc][cr][cc] = removed  # restore

        remaining = sum(
            1 for br in range(3) for bc in range(3)
              for cr in range(3) for cc in range(3)
              if puzzle[br][bc][cr][cc] != 0
        )
        if remaining <= clues:
            break

    return puzzle


   
def gen_puzzle():
    board_2d = generate_sudoku() # from earlier
    print_sudoku(board_2d)
    sfield = sudoku_to_tensor(board_2d)
    print_field(sfield)
    sfield = make_puzzle_field(sfield)
    print_field(sfield)
    return sfield

def correct(inp):
    valid_numbers = [1,2,3,4,5,6,7,8,9]
    if inp.isdigit():
        if int(inp) in valid_numbers:
            return True
        else:
            return False
    elif inp=="":
        return True
    else:
        return False



def check_sudoku():
    efieldindex=0;
    for i in range(0,3):
        for j in range(0,3):
            for k in range(0,3):
                for l in range(0,3):
                    value = efield[efieldindex].get()
                    if value=="":
                        sfield[i][j][k][l]=0
                    else:
                        sfield[i][j][k][l]=int(value)

                    efieldindex = efieldindex+1
    # print_field(sfield)
    if check_sudoku_field():
        messagebox.showinfo(title="Nice!", message="Nice!")
    else:
        messagebox.showinfo(title="Fail!", message="Fail!")

zero_field = [[[[0,0,0],[0,0,0],[0,0,0]],
           [[0,0,0],[0,0,0],[0,0,0]],
           [[0,0,0],[0,0,0],[0,0,0]]],
          [[[0,0,0],[0,0,0],[0,0,0]],
           [[0,0,0],[0,0,0],[0,0,0]],
           [[0,0,0],[0,0,0],[0,0,0]]],
          [[[0,0,0],[0,0,0],[0,0,0]],
           [[0,0,0],[0,0,0],[0,0,0]],
           [[0,0,0],[0,0,0],[0,0,0]]]]


root = Tk()
root.title("Sudoku")

mainframe = Frame(root)
mainframe.pack(padx=50, pady=(50,10))

efield = []
reg = root.register(correct)
sfield = copy.deepcopy(zero_field)
sfield = gen_puzzle()
print_field(sfield)
for i in range(0,3):
    for j in range(0,3):
        for k in range(0,3):
            for l in range(0,3):
                if sfield[i][j][k][l] == 0:
                    new_e = Entry(mainframe, font =("Calibri",25), width=2, borderwidth=1,
                    textvariable=str(i)+str(j)+str(k)+str(l),validate='key', validatecommand=(reg,'%P')
                    ,justify='center')
                else:
                    entry_text = StringVar(value=str(sfield[i][j][k][l]))
                    new_e = Entry(mainframe, font =("Calibri",25), width=2, borderwidth=1,
                    textvariable=entry_text,state='readonly',readonlybackground='white',validate='key', validatecommand=(reg,'%P')
                    ,justify='center')
                val = [[0,1,2],[3,4,5],[6,7,8]]
                new_e.grid(column=val[k][l], row=val[i][j],ipadx=10,ipady=10)
                efield.append(new_e)



button_frame = Frame(root)
button_frame.pack(pady=10)

button = Button(button_frame, text='Check', command=check_sudoku)
button.pack()

root.mainloop()
