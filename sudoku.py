#author: Daniel Rossmaier
from tkinter import messagebox
from tkinter import *

sfield = [[[[0,0,0],[0,0,0],[0,0,0]],
           [[0,0,0],[0,0,0],[0,0,0]],
           [[0,0,0],[0,0,0],[0,0,0]]],
          [[[0,0,0],[0,0,0],[0,0,0]],
           [[0,0,0],[0,0,0],[0,0,0]],
           [[0,0,0],[0,0,0],[0,0,0]]],
          [[[0,0,0],[0,0,0],[0,0,0]],
           [[0,0,0],[0,0,0],[0,0,0]],
           [[0,0,0],[0,0,0],[0,0,0]]]]

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
        print("vertical")
        print(koords)
        print(vertical)
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
        print("horizontal")
        print(koords)
        print(horizontal)
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
        print(value)
        print("cluster")
        print(koords)
        print(cluster)
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



root = Tk()
root.title("Sudoku")

mainframe = Frame(root)
mainframe.pack(padx=50, pady=(50,10))

efield = []

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

reg = root.register(correct)
for i in range(0,3):
    for j in range(0,3):
        for k in range(0,3):
            for l in range(0,3):

                new_e = Entry(mainframe, font =("Calibri",25), width=2, borderwidth=1,
                textvariable=str(i)+str(j)+str(k)+str(l),validate='key', validatecommand=(reg,'%P')
                ,justify='center')
                val = [[0,1,2],[3,4,5],[6,7,8]]
                new_e.grid(column=val[k][l], row=val[i][j],ipadx=10,ipady=10)
                efield.append(new_e)


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
    print_field(sfield)
    if check_sudoku_field():
        messagebox.showinfo(title="Nice!", message="Nice!")
    else:
        messagebox.showinfo(title="Fail!", message="Fail!")

button_frame = Frame(root)
button_frame.pack(pady=10)

button = Button(button_frame, text='Check', command=check_sudoku)
button.pack()

root.mainloop()
