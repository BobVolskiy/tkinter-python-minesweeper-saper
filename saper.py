import random
from tkinter import Label, Button, Tk, messagebox, Frame, StringVar, Entry
import time
from threading import Thread
import os
bg='#222327'
fg='#ffffff'
nearby=[]
l=[]
field=[]
font=("Montserrat Medium", 15)
def flag(event,i,j):
    global field
    if field[i][j]=='F':
        field[i][j]='.'
        buttons[(i, j)].config(text='.',bg=bg)
    elif field[i][j]=='.':
        field[i][j]='F'
        buttons[(i, j)].config(text='F',bg='#333333')
    update()
def createnewfield():
    global minecount
    minecount =0
    for i in range(size):
        l.append([])
        for j in range(size):
            if random.choice(conc) == 0:
                l[i].append(0)
            else: 
                l[i].append(1)
                minecount+=1
    for i in range(size):
        nearby.append([])
        for j in range(size):
            nearby[i].append('.')
    for i in range(size):
        field.append([])
        for j in range(size):
            field[i].append('.')
def startgame():
    global field,gamesaved, minecount,size
    
    
    minecount=0
    if gamesaved==False:
        createnewfield()
    else:
        try: 
            db = open(login_entry.get()+"_save.txt", "r")
            for line in db:
                lil=line.split()
            db.close()
            size=int(lil[3])
            k=0
            for i in range(size):
                l.append([])
                for j in range(size):
                    if lil[0][k]=='1':
                        minecount+=1
                    l[i].append(int(lil[0][k]))
                    k+=1    
            k=0
            for i in range(size):
                nearby.append([])
                for j in range(size):
                    nearby[i].append(lil[1][k])
                    k+=1
            k=0
            for i in range(size):
                field.append([])
                for j in range(size):
                    field[i].append(lil[2][k])
                    k+=1  
        except:
            createnewfield()
    window.geometry(str(30*size)+"x"+str(30*size))
    for i in range(size):
        for j in range(size):
            buttons[(i, j)]=Button(text='.',bg=bg,fg='#FF2D00',border=0,font=font, command=lambda i=i, j=j: selectmine(i,j))
            buttons[(i, j)].place(x=i*30, y=j*30, width=30, height=30)
            buttons[(i, j)].bind('<Button-3>', lambda k=1, i=i, j=j: flag(k,i,j))
    update()
    return minecount  
def countfield(x,y):
    xlist=[x-1,x,x+1]
    ylist=[y-1,y,y+1]
    counter=0
    for i in xlist:
        for j in ylist:
            if i>=0 and j>=0 and i<=size-1 and j<=size-1:
                if i!=xlist[1] or j!=ylist[1]:
                    if l[i][j]==1:
                        counter+=1                 
    return counter
def openempty(x,y):
    xlist=[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
    for i in xlist:
        if i[0]>=0 and i[1]>=0 and i[1]<=size-1 and i[0]<=size-1:
            if l[i[0]][i[1]]==0 and nearby[i[0]][i[1]]=='.':
                nearby[i[0]][i[1]]=countfield(i[0],i[1]) 
                openempty(i[0],i[1])
def sec():
    sec = 0
    minn = 0
    global stop_thread
    while True:
        if stop_thread==True:
            break
        if sec==60:
            sec=0
            minn+=1
        window.title('Мины: '+str(minecount)+'. Время: '+str(minn)+':'+str(sec))
        time.sleep(1)
        sec += 1
def restartgame():
    global l, nearby, field,minecount,stop_thread
    nearby.clear()
    l.clear()
    field.clear()
    minecount=startgame()
    stop_thread=False
    threa = Thread(target=sec)
    threa.start()
def selectmine(x,y):
    global field, stop_thread
    if field[x][y]=='.':
        if l[x][y]==1:
            for i in range(size):
                for j in range(size):
                    if l[i][j]==1:
                        field[i][j]='m'
            update()
            stop_thread=True
            os.remove(login_entry.get()+"_save.txt")
            ask=messagebox.askretrycancel("Мина", "Вы проиграли. Начать заново?",icon='error')
            for i in range(size):
                for j in range(size):
                    buttons[(i, j)].destroy()
            if ask==True:
                restartgame()
            else: 
                nearby.clear()
                l.clear()
                field.clear()
                mainmenu()
            
        else:
            openempty(x,y)
            field[x][y]=str(nearby[x][y])
            for z in range(size):
                for k in range(size):
                    if nearby[z][k]==0:
                        xlist=[z-1,z,z+1]
                        ylist=[k-1,k,k+1]
                        for i in xlist:
                            for j in ylist:
                                if i>=0 and j>=0 and i<=size-1 and j<=size-1:
                                    field[z][k]='0'
                                    field[i][j]=str(nearby[i][j])
            update()
buttons = {}
def update():
    global field, minecount, stop_thread, saving
    hidden_field=''
    nearby_field=''
    open_field=''
    for i in l:
        for j in i:
            hidden_field+=str(j)
    for i in nearby:
        for j in i:
            nearby_field+=str(j)        
    for i in field:
        for j in i:
            open_field+=str(j)
    saving = open(login_entry.get()+"_save.txt", "w")
    saving.write(hidden_field+' '+nearby_field+' '+open_field+' '+str(size))
    saving.close()
    notmine=0
    notmineflagged=0
    notopen=0
    for i in range(size):
        for j in range(size):
            bg='#222327'
            if field[i][j]=='0':
                text = ''
                fg='#ffffff'
            elif field[i][j]=='1':
                text = '1'
                fg='#82E0AA'
            elif field[i][j]=='2':
                text = '2'
                fg='#F7DC6F'
            elif field[i][j]=='3':
                text = '3'
                fg='#F5B041'
            elif field[i][j]=='4':
                text = '4'
                fg='#A93226'
            elif field[i][j]=='5':
                text = '5'
                fg='#AF7AC5'
            elif field[i][j]=='6':
                text = '6'
                fg='#3498DB'
            elif field[i][j]=='m':
                text = 'M'
                fg='#FFFFFF'
                bg='#FF2D00'
            elif field[i][j]=='F':
                text = 'F'
                if l[i][j]==1:
                    notmine+=1
                notmineflagged+=1
                fg='#FF2D00'
                bg='#333333'
            else: 
                text = field[i][j]
                notopen+=1
                fg='#FF2D00'
            buttons[(i, j)].config(text=text,bg=bg,fg=fg,border=0,font=font, command=lambda i=i, j=j: selectmine(i,j))
    if notmine==minecount and notmineflagged==minecount and notopen==0:
        stop_thread=True
        os.remove(login_entry.get()+"_save.txt")
        ask=messagebox.askretrycancel("Победа", "Вы выиграли. Начать заново?")
        for i in range(size):
                for j in range(size):
                    buttons[(i, j)].destroy()
        if ask==True:
                restartgame()
        else: 
            nearby.clear()
            l.clear()
            field.clear()
            mainmenu()
def auth():
    global gamesaved
    gamesaved=False
    if login_entry.get()!='' and password_entry.get()!='':
        found='notfound'
        try: 
            inF = open("auth.txt", "r")
        except:
            inF= open("auth.txt","w")
            inF.close()
            inF = open("auth.txt", "r")
        for line in inF:
            auth_line=line.split()
            if auth_line[0]==login_entry.get() and auth_line[1]==password_entry.get():
                print('Hello!')
                messagebox.showinfo('Привет','Привет, '+login_entry.get())
                gamesaved=True
                inF.close()
                found='found'
                restartgame()
                break
            elif auth_line[0]==login_entry.get() and auth_line[1]!=password_entry.get():
                found='wrong'
                messagebox.showinfo('Неверный пароль','Неверный пароль')
                break
        if found=='notfound':
            outF = open("auth.txt", "a")
            messagebox.showinfo('Новый пользователь!','Зарегистрирован игрок '+login_entry.get())
            outF.write(login_entry.get()+' '+password_entry.get()+"\n")
            outF.close() 
            restartgame() 
        
    else: 
        messagebox.showerror('Ошибка','Введите логин и пароль')
window = Tk()
frame=Frame(bg=bg)
login_entry = StringVar()
loginlabel=Label(frame,text='Login:',bg=bg,fg=fg,anchor='w', border=0,font=font)
login = Entry(frame,textvariable=login_entry, font=font,highlightthickness=2, bg=bg, fg=fg)
password_entry = StringVar()
passwordlabel=Label(frame,text='Password:',bg=bg,fg=fg, anchor='w', border=0,font=font)
password = Entry(frame,textvariable=password_entry, font=font,highlightthickness=2, bg=bg, fg=fg)
startb=Button(frame,text='Start Easy',bg=fg,fg=bg, border=0,font=("Montserrat Medium", 18), command=auth)           
def selector(d):
    global size
    global conc
    global minecount
    if d==1:
        size = 10
        conc=[0,0,0,0,0,1]
        startb.config(text='START EASY 10x10')
    elif d==2:
        size = 15
        conc=[0,0,0,0,1]
        startb.config(text='START MEDIUM 15x15')
    elif d==3:
        size = 25
        conc=[0,0,0,1]
        startb.config(text='START HARD 25x25')
selector(1)
def mainmenu():
    window.geometry(str(300)+"x"+str(500))
    window.title("Minesweeper")
    frame.place(x=0, y=0, width=300, height=500)
    label=Label(frame,text='Minesweeper *',bg=bg,fg=fg, border=0,font=("Montserrat Medium", 25))
    label.place(x=0, y=20, width=300, height=50)
    easyb=Button(frame,text='EASY',bg=bg,fg=fg, border=0,font=font, padx=30, command=lambda : selector(1))
    easyb.place(x=0, y=110, width=300, height=30)
    medb=Button(frame,text='MEDIUM',bg=bg,fg=fg, border=0,font=font, padx=30, command=lambda : selector(2))
    medb.place(x=0, y=140, width=300, height=30)
    hardb=Button(frame,text='HARD',bg=bg,fg=fg, border=0,font=font, padx=30, command=lambda : selector(3))
    hardb.place(x=0, y=170, width=300, height=30)
    login.place(x=30, y=280, width=240, height=30)
    loginlabel.place(x=30, y=250, width=240, height=30)
    password.place(x=30, y=350, width=240, height=30)
    passwordlabel.place(x=30, y=320, width=240, height=30)
    startb.place(x=0, y=450, width=300, height=50)
mainmenu()
window.resizable(False, False)
window.configure(background='#222327')
window.mainloop()        