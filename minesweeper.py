import random
from datetime import datetime


#This is the main function
def play():
    hs = open("C:\\Users\\sanskar\\Desktop\\Minesweeper\\high_score.txt")
    hsl = hs.readlines()
    hs.close()

    hss = int(hsl[1])*60 + int(hsl[2])
    
    bmb_e = "\U000020AA"
    bmb_f = "\U000003B6"

    print("Current highscore by",hsl[0].strip(),":",hsl[1].strip(),"minutes",hsl[2].strip(),"seconds")
    name = input("Enter your name: ")
    n = int(input("Enter the board dimension: "))
    while (n <= 0 )or(n>10):   #Board dimensions have to be positive integers
        print("Invalid dimensions!! Enter a valid number(>0 and <10).")
        n = int(input("Enter the board dimension: "))
    n_mines = int(input("Enter the number of mines you want to play with: "))
    while (n_mines > (n**2 - 1)) or (n_mines <= 0):     #Number of mines should not exceed number of squares
        print("Invalid number of mines!! Enter a valid number(<", n**2," and >0).")
        n_mines = int(input("Enter the number of mines you want to play with: "))
    dug = []

    d1 = datetime.now()
    s1 = d1.hour*3600 + d1.minute*60 + d1.second
    
    #To display the board
    #Input parameters:
    #   brd: 2D list containing the board
    def display(brd):
        
        #for header
        
        print()
        print(bmb_f*8, end="")
        for i in range(len(brd)):
            print(bmb_f*3, end="")
        print(bmb_f*2)
        print(bmb_f+bmb_e*7, end="")
        for i in range(len(brd)):
            print(bmb_e*3, end="")
        print(bmb_e+bmb_f)
        print(bmb_f+bmb_e,"    ", end="")
        for i in range(len(brd)):
            print(i," ", end="")
        print(" "+bmb_e+bmb_f)
        #for each row
        for i in range(len(brd)):
            print(bmb_f+bmb_e,i,"-|",end="")
            for j in range(len(brd)):
                if brd[i][j][1] == False:
                    show = " "
                else:
                    show = brd[i][j][0]
                print(show,"|",end="")
            print(" "+bmb_e+bmb_f)
        print(bmb_f+bmb_e,"     ", end="")
        for i in range(len(brd)):
            print("   ", end="")
        print(bmb_e+bmb_f)
        print(bmb_f+bmb_e*7, end="")
        for i in range(len(brd)):
            print(bmb_e*3, end="")
        print(bmb_e+bmb_f)
        print(bmb_f*8, end="")
        for i in range(len(brd)):
            print(bmb_f*3, end="")
        print(bmb_f*2)
        print()
    #To create the 2D list based on the input dimension
    #Input parameters:
    #   n: Dimension of the board 
    def create_board(n):
        brd = [[[None, False] for i in range(n)] for i in range(n)]
        return brd
        
    #To randomly place mines in the board
    #Input parameters:
    #   l: 2D list containing the empty board
    #   n: Number of mines
    def place_mines(l,n):
        mines_planted = 0
        while mines_planted < n:
            g = random.randint(0, len(l)**2 - 1 )
            row = g//len(l)
            col = g%len(l)
            if l[row][col][0] == "*":
                continue
            l[row][col][0] = "*"
            mines_planted += 1
        return l
        
    #To get the number of nearby mines
    #Input parameters:
    #   l: 2D list containing the board
    #   r: Row index of the box to be checked
    #   c: Column index of the box to be checked
    def get_number(l,r,c):
        num_neigh_mines = 0
        for i in range(max(0,r-1), min(len(l)-1, r+1)+1):   
            for j in range(max(0,c-1), min(len(l)-1, c+1)+1):
                if i == r and j == c:
                    continue
                if l[i][j][0] == "*":
                    num_neigh_mines += 1
        return num_neigh_mines
        
    #To assign number of mines to the game board
    #Input parameters:
    #   l: 2D list containing the board
    def assign_values(l):
        for i in range(len(l)):
            for j in range(len(l)):
                if l[i][j][0] == "*":
                    continue
                l[i][j][0] = get_number(l,i,j)
                
    #To dig at the position specified by the user recursively
    #Input parameters:
    #   l: 2D list containing the board
    #   r: Row index of the box to be dug
    #   c: Column index of the box to be dug
    def dig(l,r,c):
        if (r,c) not in dug:
            dug.append((r,c))
            
        l[r][c][1] = True
        if l[r][c][0] == "*":
            return False
        elif l[r][c][0] > 0:
            l[r][c][1] = True
            return True
        for i in range(max(0,r-1), min(len(l)-1, r+1)+1):
            for j in range(max(0,c-1), min(len(l)-1, c+1)+1):
                if (i,j) in dug:
                    continue
                l[i][j][1] = True
                dig(l,i,j)
        return True
        
    brd = create_board(n)
    brd = place_mines(brd,n_mines)
    assign_values(brd)
    
    itr = True
    while itr:
        display(brd)
        point = input("Where do you want to dig?(row,column) ").split(",")
        for i in range(len(point)):
            point[i] = int(point[i])
        while ((point[0] > n-1) or (point[1] > n-1)) or ((point[0] < 0) or (point[1] < 0)):
            print("Invalid coordinates!! Make sure row and column are >0 and less than the defined dimension.")
            point = input("Where do you want to dig?(row,column) ").split(",")
            for i in range(len(point)):
                point[i] = int(point[i])
        itr = dig(brd, point[0], point[1])
        if len(dug) == n**2 - n_mines:
            break

    d2 = datetime.now()
    s2 = d2.hour*3600 + d2.minute*60 + d2.second
    m = (s2-s1)//60
    ss = (s2-s1)%60
    
    if itr == True:
        for i in brd:
            for j in i:
                j[1] = True
        display(brd)
        print("Congrats you won!! \U0001F600\U0001F600\U0001F600 \n\U0001F556You took", m,"minutes and", ss,"seconds.\U0001F556")
        if (s2-s1)<hss:
            hs = open("C:\\Users\\sanskar\\Desktop\\Minesweeper\\high_score.txt","w")
            hs.write("%s\n"%name)
            hs.write("%s\n"%m)
            hs.write("%s\n"%ss)
            hs.close()
            print("You've made a new high score!")
        else:
            print("You couldn't beat the high score.", "Current highscore by",hsl[0].strip(),":",hsl[1].strip(),"minutes",hsl[2].strip(),"seconds")
    else:
        for i in brd:
            for j in i:
                j[1] = True
        display(brd)
        print("Mine dug\U0001F4A3\U0001F4A3\U0001F4A3!! You lost! Game over! \n\U0001F556You took", m,"minutes and", ss,"seconds.\U0001F556")
play() 