# ------------------------------ Imports ------------------------------#

from tkinter import *

# -----------------------------------------------------------------------#

# ------------------------------ Variables ------------------------------#

coos = []
val = ["a", "b", "c", "d", "e", "f", "g", "h"]
color = ["black", "white"]


# -----------------------------------------------------------------------#

# ------------------------------ Functions ------------------------------#

# creating board with coordinates
def board():
    # creating coordinates
    for j in range(1, 9):
        gridlines = []
        for i in range(1, 9):
            gridlines.append(str(val[i - 1]) + str(j))
        coos.append(gridlines)
    coos.reverse()
    for x in coos:
        print(x, end="\n")

    # creating board
    for j in range(8):
        for i in range(8):
            if (i + j) % 2 == 0:  # setting the color of boxes
                color_2 = color[0]
            else:
                color_2 = color[1]
            box = can.create_rectangle((0 + (90 * i)), (0 + (90 * j)), (90 + (90 * i)), (90 + (90 * j)), fill=color_2)


# -----------------------------------------------------------------------#

# ------------------------------ Printing  ------------------------------#

win = Tk()
win.title("Blitz")
can = Canvas(win, bg="black", height=720, width=720)
can.pack()
board()
win.mainloop()
