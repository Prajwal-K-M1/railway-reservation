from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector as con
from datetime import *
from PIL import Image, ImageTk

root = Tk()

root.geometry('1500x800')
root.minsize(1500,800)
root.maxsize(1500,800)
myFontH = ("Bahnschrift", 24, 'bold')
myFontM = ("Bahnschrift", 15, 'bold')
myFont = ("Bahnschrift", 12)


seats = [108, [27, 18, 27], [11, 11], [23, 23], [24, 16, 24]]

connection = con.connect(host="localhost", user="root", password="Prajwal@12", database="nirctc")

def hoverIn(e):
    e.widget['foreground'] = 'white'
    e.widget['background'] = 'blue'
    e.widget['font'] = myFontM

def hoverOut(e):
    e.widget['foreground'] = 'black'
    e.widget['background'] = 'SystemButtonFace'
    e.widget['font'] = myFont

def hoverInCol(e):
    e.widget['foreground'] = 'white'
    e.widget['background'] = 'orange'

def hoverInColG(e):
    e.widget['foreground'] = 'white'
    e.widget['background'] = 'green'

def hoverInColA(e):
    e.widget['foreground'] = 'white'
    e.widget['background'] = 'violet'

def hoverOutCol(e):
    e.widget['foreground'] = 'black'
    e.widget['background'] = 'SystemButtonFace'

def hoverInRd(e):
    e.widget['foreground'] = 'white'
    e.widget['background'] = 'red'

def hoverOutRd(e):
    e.widget['foreground'] = 'black'
    e.widget['background'] = 'SystemButtonFace'

f1 = PhotoImage(file='train.png')
f2 = ImageTk.PhotoImage(Image.open('train2.png'))
f3 = ImageTk.PhotoImage(Image.open('train3.png'))

class Page(Canvas):
    def __init__(self):
        super().__init__(width = 1500,
                         height = 800)
        
        self.pack()
        self.login(0)

    def login(self, flag):
        self.delete(ALL)
        root.title("Login Page")
        self.create_image(0, 0, image = f1, anchor = 'nw')
        if flag == 1:
            messagebox.showinfo("LOGGED OUT", "Thank you")
        def checklog():
            if usermail.get().strip() == 'admin' and password.get().strip() == 'admin':
                self.admin()
                return
            if usermail.get().strip() == '' or password.get().strip() == '':
                messagebox.showerror('Error', 'All fields are required')
                return
            cursor = connection.cursor()
            cursor.execute(f'select * from users where mail = "{usermail.get().strip()}" and password = "{password.get().strip()}"')
            temp = cursor.fetchone()
            userid = temp[0] if temp is not None else -1
            if userid == -1:
                messagebox.showerror('User not Found', 'Invalid credintials')
            else:
                messagebox.showinfo('Success', 'Logging in .. Click OK to continue')
                self.delete(ALL)
                self.create_text(750, 400, text = 'Loding ...', fill = 'blue', font = myFont)
                self.after(1000, self.optioner, userid)

        usermail = StringVar()
        usermail.set("")
        password = StringVar()
        password.set("")

        self.create_text(750, 250, text = 'LOGIN',font = ("Bahnschrift", 30, 'bold'))

        self.create_text(580, 350, text = 'Enter User Mail',font = ("Bahnschrift", 20, 'bold'))
        u = Entry(textvariable = usermail, font = myFont)
        self.create_window(800, 350, window = u)
        self.create_text(580, 450, text = 'Enter Password', font = ("Bahnschrift", 20, 'bold'))
        p = Entry(textvariable = password, font = myFont)
        self.create_window(800, 450, window = p)

        b = Button(width = 10, height = 2, text = "Login", font = myFont, command = checklog)
        b.bind('<Enter>', hoverIn)
        b.bind('<Leave>', hoverOut)
        self.create_window(770, 550, window = b)

        r = Button(width = 10, height = 2, text = "REGISTER", font = myFont, command = self.register)
        r.bind('<Enter>', hoverIn)
        r.bind('<Leave>', hoverOut)
        self.create_window(1400, 100, window = r)

    def admin(self):
        def dispUsers():
            def up():
                if fst[0] == 0:
                    return
                fst[0] -= 1
                lst[0] -= 1
                printer(fst[0], lst[0])
            def down():
                if lst[0] == len(ar):
                    return
                fst[0] += 1
                lst[0] += 1
                printer(fst[0], lst[0])
            def printer(i, j):
                self.delete(ALL)
                self.create_image(0, 0, image = f3, anchor = 'nw')
                root.title('IRCTC | USERS LIST')
                back = Button(text = 'BACK', command = self.admin)
                back.bind('<Enter>', hoverInRd)
                back.bind('<Leave>', hoverOutRd)
                self.create_window(100, 100, window = back)
                self.create_rectangle(500, 350, 1050, 600, fill = 'white')
                self.create_text(750, 200, text = "USERS", font = myFontH)
                bu = Button(text = 'Scroll Up', font = myFont, command = lambda: up())
                bd = Button(text = 'Scroll Down', font = myFont, command = lambda: down())
                back.bind('<Enter>', hoverInCol)
                back.bind('<Leave>', hoverOutCol)
                self.create_window(750, 300, window = bu)
                self.create_window(750, 640, window = bd)
                self.create_text(600, 380, font = myFont,  text = "USER ID")
                self.create_text(750, 380, font = myFont,  text = "USER NAME OR MAIL")
                self.create_text(950, 380, font = myFont, text = "PASSWORD")
                ht = 440
                for x in range(i, j):
                    self.create_text(600, ht, font = myFont, text = ar[x][0])
                    self.create_text(750, ht, font = myFont, text = ar[x][1])
                    self.create_text(950, ht, font = myFont, text = ar[x][2])
                    ht += 60

            self.delete(ALL)
            cursor = connection.cursor()
            cursor.execute('select * from users')
            ele = cursor.fetchall()
            ar = []
            for i in ele:
                ar.append([i[0], i[1], i[2]])
            fst, lst = [0], [0]
            if len(ar) > 3:
                lst = [3]
            else:
                lst = [len(ar)]
            printer(fst[0], lst[0])

        def trainDetailsAdmin():

            def hi(e):
                e.widget['background'] = 'yellowgreen'

            def ho(e):
                e.widget['background'] = 'SystemButtonFace'

            def up():
                if fst[0] == 0:
                    return
                fst[0] -= 1
                lst[0] -= 1
                printT()
                
            def down():
                if lst[0] == len(ar):
                    return
                fst[0] += 1
                lst[0] += 1
                printT()

            def upDD():
                if fst[0] == 0:
                    return
                fst[0] -= 1
                lst[0] -= 1
                printDD()
                
            def downDD():
                if lst[0] == len(ar):
                    return
                fst[0] += 1
                lst[0] += 1
                printDD()

            def printT():
                self.delete(ALL)
                root.title("IRCTC")
                self.create_image(0, 0, image = f2, anchor = 'nw')
                back = Button(text = 'BACK', command = trainDetailsAdmin)
                back.bind('<Enter>', hoverInRd)
                back.bind('<Leave>', hoverOutRd)
                self.create_window(100, 100, window = back)
                self.create_text(550, 100, text = 'Select Date : ', font = myFontM, fill = 'white')
                self.create_window(720, 100, window = dt)
                self.create_window(900, 100, window = btn)

                self.create_rectangle(600, 350, 900, 600, fill = 'white')
                self.create_text(750, 200, text = "SELECT A TRAIN", font = myFontH)
                bu = Button(text = 'Scroll Up', font = myFont, command = lambda: up())
                bu.bind('<Enter>', hoverInCol)
                bu.bind('<Leave>', hoverOutCol)
                bd = Button(text = 'Scroll Down', font = myFont, command = lambda: down())
                bd.bind('<Enter>', hoverInCol)
                bd.bind('<Leave>', hoverOutCol)
                self.create_window(750, 300, window = bu)
                self.create_window(750, 640, window = bd)
                self.create_text(650, 380, font = myFont,  text = "SL NO")
                self.create_text(780, 380, font = myFont,  text = "TRAIN NAME")
                ht = 440
                for x in range(fst[0], lst[0]):
                    self.create_text(650, ht, font = myFont, text = str(x+1))
                    temp = Button(text = ar[x], font = myFont)
                    temp.bind('<Enter>', hi)
                    temp.bind('<Leave>', ho)
                    temp.bind('<Button>', lambda x: printD(x))
                    self.create_window(780, ht, window = temp)
                    ht += 60

            def printD(e):
                tr = e.widget['text']   
                cursor = connection.cursor()
                cursor.execute(f'select trainno from train where trainname = "{tr}"')
                trn = cursor.fetchone()[0]
                mm, dd, yy = dt.get().split('/')
                cursor.execute(f'select * from ticket where trainno = {trn} and traveldate = "20{yy}-{mm}-{dd}"')
                ele = cursor.fetchall()
                fst[0] = 0
                ar.clear()
                for i in ele:
                    ar.append([i[1], i[2], i[4], i[6], i[7], i[9], i[10]])
                if len(ar) > 3:
                    lst[0] = 3
                else:
                    lst[0] = len(ar)
                printDD()

            def printDD():
                self.delete(ALL)
                root.title("IRCTC")
                self.create_image(0, 0, image = f2, anchor = 'nw')
                back = Button(text = 'BACK', command = trainDetailsAdmin)
                back.bind('<Enter>', hoverInRd)
                back.bind('<Leave>', hoverOutRd)
                self.create_window(100, 100, window = back)
                mm, dd, yy = dt.get().split('/')
                self.create_text(750, 100, text = f'{dd} - {mm} - 20{yy}', font = myFontH, fill = 'white')
                self.create_rectangle(370, 350, 1250, 600, fill = 'white')
                self.create_text(750, 200, text = "DETAILS", font = myFontH)
                bu = Button(text = 'Scroll Up', font = myFont, command = lambda: upDD())
                bd = Button(text = 'Scroll Down', font = myFont, command = lambda: downDD())
                bu.bind('<Enter>', hoverInCol)
                bu.bind('<Leave>', hoverOutCol)
                bd.bind('<Enter>', hoverInCol)
                bd.bind('<Leave>', hoverOutCol)
                self.create_window(750, 300, window = bu)
                self.create_window(750, 640, window = bd)
                self.create_text(450, 380, font = myFont,  text = "PNR")
                self.create_text(550, 380, font = myFont,  text = "NAME")
                self.create_text(690, 380, font = myFont,  text = "ADHAR")
                self.create_text(800, 380, font = myFont,  text = "USER ID")
                self.create_text(900, 380, font = myFont,  text = "CONFIRMED")
                self.create_text(1000, 380, font = myFont,  text = "TYPE")
                ht = 440
                for x in range(fst[0], lst[0]):
                    self.create_text(450, ht, font = myFont, text = ar[x][0])
                    self.create_text(550, ht, font = myFont,  text = ar[x][1])
                    self.create_text(690, ht, font = myFont,  text = ar[x][2])
                    self.create_text(800, ht, font = myFont,  text = ar[x][3])
                    self.create_text(900, ht, font = myFont,  text = 'YES' if ar[x][4] == 1 else 'NO')
                    self.create_text(1000, ht, font = myFont,  text = ar[x][5].upper() + (' - ' + ar[x][6].upper() if ar[x][6] is not None else ''))
                    cpB = Button(text = f"PNR - {ar[x][0]}\nCopy to Clipboard")
                    cpB.bind('<Enter>', hi)
                    cpB.bind('<Leave>', ho)
                    cpB.bind('<Button>', cpyCB)
                    self.create_window(1140, ht, window = cpB)
                    ht += 60

            def cpyCB(s):
                root.clipboard_clear()
                pnr = s.widget['text'].split('\n')[0][-10:]
                root.clipboard_append(pnr)
                messagebox.showinfo('Copied', f'PNR - {pnr} is copied to your clipboard')
                printDD()

            self.delete(ALL)
            root.title("IRCTC")
            self.create_image(0, 0, image = f2, anchor = 'nw')
            back = Button(text = 'BACK', command = self.admin)
            back.bind('<Enter>', hoverInRd)
            back.bind('<Leave>', hoverOutRd)
            self.create_window(100, 100, window = back)

            fst, lst = [0], [0]
            cursor = connection.cursor()
            cursor.execute('select trainname from train')
            ele = cursor.fetchall()
            ar = []
            for i in ele:
                ar.append(i[0])
            if len(ar) > 3:
                lst = [3]
            else:
                lst = [len(ar)]

            self.create_text(550, 100, text = 'Select Date : ', font = myFontM, fill = 'white')
            dt = DateEntry(font = myFontM)
            self.create_window(720, 100, window = dt)
            btn = Button(text = 'Search', font = myFont, command = printT)
            btn.bind('<Enter>', hoverInColG)
            btn.bind('<Leave>', hoverOutCol)
            self.create_window(900, 100, window = btn)

        def addTrain():
            
            def checkValid():
                try:
                    a = int(gen.get())
                    a = int(slp.get())
                    a = int(ac1.get())
                    a = int(ac2.get())
                    a = int(ac3.get())
                except:
                    messagebox.showerror("Error","Fair should be a number (Integer)")
                    return
                if len(trainNo.get()) != 6:
                    messagebox.showerror("Invalid input","Length of train number must be 6")
                    return
                cursor = connection.cursor()
                cursor.execute(f"insert into train (trainno, trainname, source, destination, general, sleeper, ac1, ac2, ac3) values ('{trainNo.get()}', '{trainName.get()}', '{source.get()}', '{desti.get()}', {int(gen.get())}, {int(slp.get())}, {int(ac1.get())}, {int(ac2.get())}, {int(ac3.get())})")
                connection.commit()
                messagebox.showinfo("Success", "Train Added Successfully")
                self.admin()

            self.delete(ALL)
            root.title("IRCTC | ADMIN - ADD TRAIN DETAILS")
            self.create_image(0, 0, image = f1, anchor = 'nw')
            trainNo = StringVar()
            trainName = StringVar()
            source = StringVar()
            desti = StringVar()
            gen = StringVar()
            slp = StringVar()
            ac1 = StringVar()
            ac2 = StringVar()
            ac3 = StringVar()

            trno = Entry(textvariable = trainNo, font = myFont)
            trna = Entry(textvariable = trainName, font = myFont)
            trs = Entry(textvariable = source, font = myFont)
            trd = Entry(textvariable = desti, font = myFont)
            trge = Entry(textvariable = gen, font = myFont)
            trsl = Entry(textvariable = slp, font = myFont)
            tra1 = Entry(textvariable = ac1, font = myFont)
            tra2 = Entry(textvariable = ac2, font = myFont)
            tra3 = Entry(textvariable = ac3, font = myFont)

            backBtn = Button(text = 'BACK', command = self.admin)
            backBtn.bind('<Enter>', hoverInRd)
            backBtn.bind('<Leave>', hoverOutRd)
            self.create_window(100, 100, window = backBtn)
            self.create_text(600, 200, text = 'Train Number', font = myFontM)
            self.create_window(800, 200, window = trno)

            self.create_text(600, 250, text = 'Train Name', font = myFontM)
            self.create_window(800, 250, window = trna)

            self.create_text(600, 300, text = 'Source', font = myFontM)
            self.create_window(800, 300, window = trs)

            self.create_text(600, 350, text = 'Destination', font = myFontM)
            self.create_window(800, 350, window = trd)

            self.create_text(600, 450, text = 'General Fair', font = myFontM)
            self.create_window(800, 450, window = trge)

            self.create_text(600, 500, text = 'Sleeper Fair', font = myFontM)
            self.create_window(800, 500, window = trsl)

            self.create_text(600, 550, text = 'AC1 Fair', font = myFontM)
            self.create_window(800, 550, window = tra1)

            self.create_text(600, 600, text = 'AC2 Fair', font = myFontM)
            self.create_window(800, 600, window = tra2)

            self.create_text(600, 650, text = 'AC3 Fair', font = myFontM)
            self.create_window(800, 650, window = tra3)

            sbtBtn = Button(text = 'ADD', command = checkValid)
            self.create_window(750, 700, window = sbtBtn)

        self.delete(ALL)
        back = Button(text = 'LOGOUT FROM ADMIN', command = lambda:self.login(1))
        back.bind('<Enter>', hoverInRd)
        back.bind('<Leave>', hoverOutRd)
        self.create_window(100, 100, window = back)
        root.title("IRCTC | ADMIN")
        self.create_image(0, 0, image = f3, anchor = 'nw')

        btnAddT = Button(text = 'Add Train', font = myFontM, command = addTrain)
        btnAddT.bind('<Enter>', hoverInColA)
        btnAddT.bind('<Leave>', hoverOutCol)
        btnSU = Button(text = 'Show users', font = myFontM, command = dispUsers)
        btnSU.bind('<Enter>', hoverInColA)
        btnSU.bind('<Leave>', hoverOutCol)
        btnGTD = Button(text = 'Get Train Details', font = myFontM, command = trainDetailsAdmin)
        btnGTD.bind('<Enter>', hoverInColA)
        btnGTD.bind('<Leave>', hoverOutCol)
        btnCPNR = Button(text = 'Check PNR Status', font = myFontM, command = lambda:self.pnrStatus(0))
        btnCPNR.bind('<Enter>', hoverInColA)
        btnCPNR.bind('<Leave>', hoverOutCol)
        btnCancel = Button(text = 'Cancel Ticket', font = myFontM, command = lambda:self.cancelTicket(0))
        btnCancel.bind('<Enter>', hoverInColA)
        btnCancel.bind('<Leave>', hoverOutCol)

        self.create_window(750, 200, window = btnAddT)
        self.create_window(750, 300, window = btnSU)
        self.create_window(750, 400, window = btnGTD)
        self.create_window(750, 500, window = btnCPNR)
        self.create_window(750, 600, window = btnCancel)

    def register(self):

        def helper():
            if mail.get().strip() == '' or password.get().strip() == '':
                messagebox.showerror("ERROR", 'All fields required')
                return
            if len(password.get().strip()) <= 4:
                messagebox.showinfo("NOTE", 'Password length must be atleast 5')
                return
            cursor = connection.cursor()
            cursor.execute(f'insert into users (mail, password) values ("{mail.get().strip()}", "{password.get().strip()}")')
            connection.commit()
            messagebox.showinfo("SUCCESS", "Registered!!!")
            self.login(0)

        self.delete(ALL)
        root.title("REGISTER TO IRCTC")
        self.create_image(0, 0, anchor = 'nw', image = f2)

        mail, password = StringVar(), StringVar()
        mail.set("")
        password.set("")
        email = Entry(textvariable = mail, font = myFont)
        epassword = Entry(textvariable = password, font = myFont)
        self.create_text(750, 300, text = "REGISTER", font = myFontH)
        self.create_text(600, 400, text = "MAIL", font = myFontM)
        self.create_text(600, 500, text = "PASSWORD", font = myFontM)
        self.create_window(780, 400, window = email)
        self.create_window(780, 500, window = epassword)
        back = Button(text = 'BACK', command = lambda:self.login(0))
        back.bind('<Enter>', hoverInRd)
        back.bind('<Leave>', hoverOutRd)
        self.create_window(100, 100, window = back)
        submit = Button(text = 'REGISTER', command = helper, font = myFontM)
        submit.bind('<Enter>', hoverInColG)
        submit.bind('<Leave>', hoverOutCol)
        self.create_window(750, 600, window = submit)

    def optioner(self, userid):
        back = Button(text = 'BACK', command = lambda:self.login(1))
        back.bind('<Enter>', hoverInRd)
        back.bind('<Leave>', hoverOutRd)
        checkStatus = Button(text = 'Check PNR Status', command = lambda: self.pnrStatus(userid), font = ("Bahnschrift", 15, 'bold'))
        bookTicket = Button(text = 'Ticket Booking', command = lambda: self.dispTicket(userid), font = ("Bahnschrift", 15, 'bold'))
        cancelTicket = Button(text = 'Ticket Cancelation', command = lambda: self.cancelTicket(userid), font = ("Bahnschrift", 15, 'bold'))
        checkStatus.bind('<Enter>', hoverInCol)
        bookTicket.bind('<Enter>', hoverInCol)
        cancelTicket.bind('<Enter>', hoverInCol)
        checkStatus.bind('<Leave>', hoverOutCol)
        bookTicket.bind('<Leave>', hoverOutCol)
        cancelTicket.bind('<Leave>', hoverOutCol)


        self.delete(ALL)
        root.title("IRCTC | HOME")
        self.create_image(0, 0, image = f2, anchor = 'nw')
        self.create_window(100, 100, window = back)
        self.create_window(750, 350, window = checkStatus)
        self.create_window(750, 450, window = bookTicket)
        self.create_window(750, 550, window = cancelTicket)

    def dispTicket(self, userid):

        def up():
            if fst[0] == 0:
                return
            fst[0] -= 1
            lst[0] -= 1
            disp(ar, fst[0], lst[0], btnUp, btnDown)


        def down():
            if lst[0] == len(ar):
                return
            fst[0] += 1
            lst[0] += 1
            disp(ar, fst[0], lst[0], btnUp, btnDown)


        def disp(ar, i, j, bu, bd):
            self.delete(ALL)
            root.title("IRCTC | TRAIN DETAILS")
            self.create_image(0, 0, image = f2, anchor = 'nw')
            back = Button(text = 'BACK', command = lambda:self.optioner(userid))
            back.bind('<Enter>', hoverInRd)
            back.bind('<Leave>', hoverOutRd)
            self.create_rectangle(400, 350, 1160, 600, fill = 'white')
            self.create_window(100, 100, window = back)
            self.create_text(750, 200, text = "Follwing Trains are available", font = myFontH)
            self.create_window(750, 300, window = bu)
            self.create_window(750, 640, window = bd)
            self.create_text(460, 380, font = myFont,  text = "SL NO.")
            self.create_text(560, 380, font = myFont,  text = "TRAIN NO.")
            self.create_text(750, 380, font = myFont,  text = "TRAIN NAME")
            self.create_text(920, 380, font = myFont,  text = "From Station")
            self.create_text(1080, 380, font = myFont, text = "To Station")
            ht = 440
            for x in range(i, j):
                self.create_text(460, ht, font = myFont, text = str(x+1))
                self.create_text(560, ht, font = myFont, text = ar[x][0])
                self.create_text(750, ht, font = myFont, text = ar[x][1])
                self.create_text(920, ht, font = myFont, text = ar[x][2])
                self.create_text(1080, ht, font = myFont,  text = ar[x][3])
                ht += 60
            btnProceed = Button(text = "Proceed for booking", command = lambda:self.loggedIn(userid), font = myFont, height = 1, width = 20)
            btnProceed.bind('<Enter>', hoverIn)
            btnProceed.bind('<Leave>', hoverOut)
            self.create_window(1200, 700, window = btnProceed)

        cursor = connection.cursor()
        cursor.execute('select * from train')
        trains = cursor.fetchall()
        ar = []
        for i in trains:
            ar.append([i[0], i[1], i[2], i[3]])
        fst, lst = [0], [0]
        if len(ar) > 3:
            lst = [3]
        else:
            lst = [len(ar)]
        btnUp = Button(text = 'Scroll Up', font = myFont, command = lambda: up())
        btnDown = Button(text = 'Scroll Down', font = myFont, command = lambda: down())
        btnUp.bind('<Enter>', hoverInColA)
        btnUp.bind('<Leave>', hoverOutCol)
        btnDown.bind('<Enter>', hoverInColA)
        btnDown.bind('<Leave>', hoverOutCol)
        disp(ar, fst[0], lst[0], btnUp, btnDown)

    def loggedIn(self, userid, *extra):
        self.delete(ALL)
        root.title("IRCTC | TICKET BOOKING")
        self.create_image(0, 0, image = f3, anchor = 'nw')
        back = Button(text = 'BACK', command = lambda:self.dispTicket(userid))
        back.bind('<Enter>', hoverInRd)
        back.bind('<Leave>', hoverOutRd)
        self.create_window(100, 100, window = back)
        cities = set()
        cursor = connection.cursor()
        cursor.execute('select source, destination from train')
        ele = cursor.fetchall()
        if not ele:
            messagebox.showerror('Error', 'No Trains found')
            self.delete(ALL)
            return
        for i in ele:
            for j in i:
                cities.add(j)

        def update(s, lb):
            s = s.strip().lower()
            lb.delete(0, 'end')
            for i in cities:
                if s in i.lower():
                    lb.insert('end', i)

        def displaylbf(lbf):
            update(travelfrom.get(), lbf)
            etravelfrom.bind('<KeyRelease>', lambda x:update(x.widget.get(), lbf))
            self.create_window(800, 440, window = lbf, tag = 'lbf')

        def nonDisplaylbf(lbf):
            self.delete(lbf)

        def displaylbt(lbt):
            update(travelto.get(), lbt)
            etravelto.bind('<KeyRelease>', lambda x:update(x.widget.get(), lbt))
            self.create_window(800, 540, window = lbt, tag = 'lbt')

        def nonDisplaylbt(lbt):
            self.delete(lbt)

        traveldate = DateEntry(font = myFont)
        travelfrom = StringVar()
        travelto = StringVar()
        if len(extra) > 0:
            mm, dd, yy = extra[2].split('/')
            traveldate = DateEntry(year = int(f'20{yy}'), month = int(mm), day = int(dd), font = myFont)
            travelfrom.set(extra[0])
            travelto.set(extra[1])
        else:
            travelfrom.set("")
            travelto.set("")
        etravelfrom = Entry(textvariable = travelfrom, font = myFont)
        lbfrom = Listbox(height = 3)
        for i in cities:
            lbfrom.insert('end', i)
        etravelfrom.bind('<FocusIn>', lambda x: displaylbf(lbfrom))
        etravelfrom.bind('<FocusOut>', lambda x: nonDisplaylbf('lbf'))
        etravelto = Entry(textvariable = travelto, font = myFont)
        lbto = Listbox(height = 3)
        for i in cities:
            lbto.insert('end', i)
        etravelto.bind('<FocusIn>', lambda x: displaylbt(lbto))
        etravelto.bind('<FocusOut>', lambda x: nonDisplaylbt('lbt'))
        self.create_text(600, 300, text = 'Enter Date of travel', font = myFont)
        self.create_window(800, 300, window = traveldate)
        self.create_text(600, 400, text = 'From', font = myFont)
        self.create_window(800, 400, window = etravelfrom)
        self.create_text(600, 500, text = 'To', font = myFont)
        self.create_window(800, 500, window = etravelto)
        btnSbt = Button(text = 'Search', width = 7, font = myFontM,  command = lambda:self.searchTrains(userid, travelfrom.get().strip(), travelto.get().strip(), traveldate.get(), cities))
        btnSbt.bind('<Enter>', hoverInColG)
        btnSbt.bind('<Leave>', hoverOutCol)
        self.create_window(750, 600, window = btnSbt)
        
    def searchTrains(self, userid, travelfrom, travelto, traveldate, cities):
        if(travelfrom.title() not in cities or travelto.title() not in cities):
            messagebox.showerror("Error", "Enter a valid available city")
            return
        cursor = connection.cursor()
        cursor.execute(f"select * from train where source = '{travelfrom.title()}' and destination = '{travelto.title()}'")
        resTrain = cursor.fetchone()
        if resTrain is None:
            messagebox.showerror("Error", "No Trains available!")
            return
        self.delete(ALL)
        root.title("IRCTC | BOOKING IN PROGRESS")
        self.create_image(0, 0, image = f1, anchor = 'nw')
        btnBack = Button(text = 'BACK', command = lambda:self.loggedIn(userid, travelfrom.title(), travelto.title(), traveldate))
        btnBack.bind('<Enter>', hoverInRd)
        btnBack.bind('<Leave>', hoverOutRd)
        self.create_window(100, 100, window = btnBack)
        tempSeats = [seats[0]]
        for i in seats[1:]:
            tempSeats.append(list(i))
        mm, dd, yy = traveldate.split('/')
        cursor = connection.cursor()
        cursor.execute(f"select * from ticket where trainno = '{resTrain[0]}' and traveldate = '20{yy}-{mm}-{dd}'")
        resTicket = cursor.fetchall()
        if resTicket is not None:
            for i in resTicket:
                if i[9] == 'general' and tempSeats[0] > 0:
                    tempSeats[0] -= 1
                elif i[9] == 'sleeper':
                    if i[10] == 'u' and tempSeats[1][0] > 0:
                        tempSeats[1][0] -= 1
                    elif i[10] == 'm' and tempSeats[1][1] > 0:
                        tempSeats[1][1] -= 1
                    elif tempSeats[1][2] > 0:
                        tempSeats[1][2] -= 1
                elif i[9] == 'ac1':
                    if i[10] == 'u' and tempSeats[2][0] > 0:
                        tempSeats[2][0] -= 1
                    elif tempSeats[2][1] > 0:
                        tempSeats[2][1] -= 1
                elif i[9] == 'ac2':
                    if i[10] == 'u' and tempSeats[3][0] > 0:
                        tempSeats[3][0] -= 1
                    elif tempSeats[3][1] > 0:
                        tempSeats[3][1] -= 1
                else:
                    if i[10] == 'u' and tempSeats[4][0] > 0:
                        tempSeats[4][0] -= 1
                    elif i[10] == 'm' and tempSeats[4][1] > 0:
                        tempSeats[4][1] -= 1
                    elif i[10] == 'l' and tempSeats[4][2] > 0:
                        tempSeats[4][2] -= 1
        gen = Button(font = myFont, text = f"General\nAvailable {tempSeats[0]}", command = lambda:self.typer(userid, resTrain[0], travelfrom.title(), travelto.title(), traveldate, 'general', tempSeats[0]))
        sle = Button(font = myFont, text = f"Sleeper\nAvailable U - {tempSeats[1][0]}, M - {tempSeats[1][1]}, L - {tempSeats[1][2]}", command = lambda:self.typer(userid, resTrain[0], travelfrom.title(), travelto.title(), traveldate, 'sleeper', tempSeats[1]))
        ac1 = Button(font = myFont, text = f"1A\nAvailable U - {tempSeats[2][0]}, L - {tempSeats[2][1]}", command = lambda:self.typer(userid, resTrain[0], travelfrom.title(), travelto.title(), traveldate, 'ac1', tempSeats[2]))
        ac2 = Button(font = myFont, text = f"2A\nAvailable U - {tempSeats[3][0]}, L - {tempSeats[3][1]}", command = lambda:self.typer(userid, resTrain[0], travelfrom.title(), travelto.title(), traveldate, 'ac2', tempSeats[3]))
        ac3 = Button(font = myFont, text = f"3A\nAvailable U - {tempSeats[4][0]}, M - {tempSeats[4][1]}, L - {tempSeats[4][2]}", command = lambda:self.typer(userid, resTrain[0], travelfrom.title(), travelto.title(), traveldate, 'ac3', tempSeats[4]))

        gen.bind('<Enter>', hoverInCol)
        gen.bind('<Leave>', hoverOutCol)

        sle.bind('<Enter>', hoverInCol)
        sle.bind('<Leave>', hoverOutCol)

        ac1.bind('<Enter>', hoverInCol)
        ac1.bind('<Leave>', hoverOutCol)

        ac2.bind('<Enter>', hoverInCol)
        ac2.bind('<Leave>', hoverOutCol)

        ac3.bind('<Enter>', hoverInCol)
        ac3.bind('<Leave>', hoverOutCol)

        self.create_window(750, 200, window = gen)
        self.create_window(750, 300, window = sle)
        self.create_window(750, 400, window = ac1)
        self.create_window(750, 500, window = ac2)
        self.create_window(750, 600, window = ac3)

    def typer(self, userid, trainno, travelfrom, travelto, traveldate, type1, nseats):
        if type1 == 'general':
            self.bookTicket(userid, trainno, travelfrom, travelto, traveldate, type1, None, nseats)
        else:
            self.delete(ALL)
            root.title("IRCTC | BOOKING IN PROGRESS")
            self.create_image(0, 0, image = f1, anchor = 'nw')
            btnBack = Button(text = 'BACK', command = lambda:self.loggedIn(userid, travelfrom, travelto, traveldate))
            btnBack.bind('<Enter>', hoverInRd)
            btnBack.bind('<Leave>', hoverOutRd)
            self.create_window(100, 100, window = btnBack)
            b1 = Button(font = myFont, text = f"UPPER ({nseats[0]} Left)", command = lambda:self.bookTicket(userid, trainno, travelfrom, travelto, traveldate, type1, 'u', nseats[0]))
            b3 = Button(font = myFont, text = f"LOWER ({nseats[-1]} Left)", command = lambda:self.bookTicket(userid, trainno, travelfrom, travelto, traveldate, type1, 'l', nseats[-1]))
            b1.bind('<Enter>', hoverInCol)
            b1.bind('<Leave>', hoverOutCol)
            b3.bind('<Enter>', hoverInCol)
            b3.bind('<Leave>', hoverOutCol)
            self.create_window(750, 300, window = b1)
            self.create_window(750, 500, window = b3)
            if type1 == 'sleeper' or type1 == 'ac3':
                b2 = Button(font = myFont, text = f"MIDDLE ({nseats[-2]} Left)", command = lambda:self.bookTicket(userid, trainno, travelfrom, travelto, traveldate, type1, 'm', nseats[-2]))
                b2.bind('<Enter>', hoverInCol)
                b2.bind('<Leave>', hoverOutCol)
                self.create_window(750, 400, window = b2)
            
    def bookTicket(self, userid, trainno, travelfrom, travelto, traveldate, type1, type2, nseats):
        self.delete(ALL)
        root.title("IRCTC | BOOKING IN PROGRESS")
        self.create_image(0, 0, image = f2, anchor = 'nw')
        btnBack = Button(text = 'BACK', command = lambda:self.loggedIn(userid, travelfrom, travelto, traveldate))
        btnBack.bind('<Enter>', hoverInRd)
        btnBack.bind('<Leave>', hoverOutRd)
        self.create_window(100, 100, window = btnBack)
        pname = StringVar()
        pname.set("")
        page = StringVar()
        page.set("")
        padhar = StringVar()
        padhar.set("")

        self.create_text(620, 300, font = myFont, text = 'Name')
        epname = Entry(font = myFontM, textvariable = pname)
        self.create_window(800, 300, window = epname)
        self.create_text(620, 400, font = myFont, text = 'Age')
        epage = Entry(font = myFontM, textvariable = page)
        self.create_window(800, 400, window = epage)
        self.create_text(1100, 400, font = myFont, text = 'Note : This should be an Valid Number')
        self.create_text(610, 500, font = myFont, text = 'Adhar Number')
        epadhar = Entry(font = myFontM, textvariable = padhar)
        self.create_window(800, 500, window = epadhar)
        submit = Button(text = 'Submit', command = lambda:self.genTicket(userid, trainno, traveldate, pname.get().strip(), page.get().strip(), padhar.get().strip(), type1, type2, nseats))
        submit.bind('<Enter>', hoverIn)
        submit.bind('<Leave>', hoverOut)
        self.create_window(750, 600, window = submit)
    
    def genTicket(self, userid, trainno, traveldate, name, age, adhar, type1, type2, nseats):
        if len(name) == 0 or len(age) == 0 or len(adhar) == 0:
            messagebox.showerror("Error", "ALL FIELDS ARE REQUIRED")
            return
        try:
            age = int(age)
        except:
            messagebox.showerror('Error', 'Enter a number for age')
            return
        if len(adhar.strip()) != 12:
            messagebox.showerror('Error', 'Enter a valid adhar number')
            return
        cursor = connection.cursor()
        pnr = (datetime.now().strftime("%f") * 2)[:10]
        confirm = 1 if nseats > 0 else 0
        mm, dd, yy = traveldate.split('/')
        if type1 == 'general':
            cursor.execute(f"insert into ticket (pnr,pname,page,padhar,trainno,uid,confirmed,traveldate,type_1 , type_2) values ('{pnr}', '{name}', '{age}', '{adhar}', '{trainno}', {userid}, {confirm}, '20{yy}-{mm}-{dd}', 'general', NULL)")
        else:
            cursor.execute(f"insert into ticket (pnr,pname,page,padhar,trainno,uid,confirmed,traveldate,type_1 , type_2) values ('{pnr}', '{name}', '{age}', '{adhar}', '{trainno}', {userid}, {confirm}, '20{yy}-{mm}-{dd}', '{type1}', '{type2}')")
        connection.commit()
        messagebox.showinfo("Booked!", "Your Ticket is booked Successfully")
        self.showDetails(userid, pnr)

    def showDetails(self, userid, pnr):

        def cpyCB(s):
            root.clipboard_clear()
            root.clipboard_append(s)
            messagebox.showinfo('Copied', f'PNR - {s} is copied to your clipboard')
            return

        self.delete(ALL)
        self.create_image(0, 0, image = f3, anchor = 'nw')
        root.title("IRCTC | TICKET BOOKED SUCCESSFULLY")
        self.create_rectangle(550, 190, 950, 730, fill = 'white')
        cursor = connection.cursor()
        cursor.execute(f"select * from ticket where pnr = '{pnr}'")
        ele = cursor.fetchone()
        cursor = connection.cursor()
        cursor.execute(f"select source, destination, {ele[9]} from train where trainno = '{ele[5]}'")
        s, d, p = cursor.fetchone()
        yy, mm, dd = str(ele[8]).split('-')
        cpyBtn = Button(text = "Click here the copy your pnr", command = lambda: cpyCB(pnr))
        cpyBtn.bind('<Enter>', hoverInCol)
        cpyBtn.bind('<Leave>', hoverOutCol)
        self.create_window(750, 250, window = cpyBtn)
        self.create_text(750, 220, text = f"PNR Number : {pnr}", font = myFont)
        self.create_text(750, 300, text = f"Train Number : {ele[5]} [{s} to {d}]", font = myFont)
        self.create_text(750, 380, text = f"Travel Date : {dd}/{mm}/{yy}", font = myFont)
        if ele[9] == 'general':
            self.create_text(750, 460, text = f"Type : General", font = myFont)
        else:
            loc = ''
            if ele[10] == 'u':
                loc = 'UPPER'
            elif ele[10] == 'm':
                loc = 'MIDDLE'
            else:
                loc = 'LOWER'
            self.create_text(750, 460, text = f"Type : {ele[9].upper()} - {loc}", font = myFont)
        self.create_text(750, 540, text = f"Ticket Status : {'Confirmed' if ele[7] == 1 else 'Waiting'}", font = myFont)
        self.create_text(750, 620, text = f"Total Amount : Rs.{p}", font = myFont)
        btn = Button(text = "OK", command = lambda: self.optioner(userid), bg = 'aqua')
        self.create_window(750, 700, window = btn)

    def pnrStatus(self, userid):

        def checkStatus():  
            if len(pnr.get().strip()) != 10:
                messagebox.showerror("INVALID PNR", 'Enter a valid PNR')
                return
            cursor = connection.cursor()
            cursor.execute(f'select * from ticket where pnr = "{pnr.get().strip()}"')
            ele = cursor.fetchone()
            if ele is None:
                messagebox.showerror("PNR Not Found", 'Enter PNR does not exist!!!')
                return
            self.delete(ALL)
            self.create_image(0, 0, image = f2, anchor = 'nw')
            self.create_rectangle(550, 160, 950, 640, fill = 'white')
            self.create_text(750, 200, text = f"PNR - {pnr.get().strip()}, Train Number - {ele[5]}", font = myFont)
            self.create_text(750, 300, text = f"Name : {ele[2]}, Age : {ele[3]}", font = myFont)
            self.create_text(750, 400, text = f"Adhar Number : {ele[4]}", font = myFont)
            self.create_text(750, 500, text = f"Date : {ele[8]}", font = myFont)
            if ele[7] == 1:
                self.create_text(750, 600, text = f"Status : Confirmed", font = myFont)
            else:
                cursor = connection.cursor()
                cursor.execute(f'select * from ticket where trainno = "{ele[5]}" and traveldate = "{str(ele[8])}" and confirmed = 0')
                elem = cursor.fetchall()
                k = 0
                for i in elem:
                    if i[1] == pnr.get().strip():
                        k = elem.index(i) + 1
                        break
                self.create_text(750, 600, text = f"Status : Waiting(w{k})", font = myFont)
            self.create_window(100, 100, window = backBtn)

        self.delete(ALL)
        self.create_image(0, 0, image = f1, anchor = 'nw')
        root.title("IRCTC | PNR STATUS")
        pnr = StringVar()
        pnr.set("")
        epnr = Entry(textvariable = pnr, font = myFont)
        self.create_text(750, 350, text = 'Enter PNR Number', font = myFontH)
        self.create_window(750, 450, window = epnr)
        sbt = Button(text = "Check Status", command = checkStatus, font = myFont)
        sbt.bind('<Enter>', hoverInColG)
        sbt.bind('<Leave>', hoverOutCol)
        self.create_window(750, 550, window = sbt)
        backBtn = -1
        if userid != 0:
            backBtn = Button(text = "BACK", command = lambda: self.optioner(userid))
            backBtn.bind('<Enter>', hoverInRd)
            backBtn.bind('<Leave>', hoverOutRd)
            self.create_window(100, 100, window = backBtn)
        else:
            backBtn = Button(text = "BACK", command = self.admin)
            backBtn.bind('<Enter>', hoverInRd)
            backBtn.bind('<Leave>', hoverOutRd)
            self.create_window(100, 100, window = backBtn)

    def cancelTicket(self, userid):
        def processDelete(pnr):
            if len(pnr) != 10:
                messagebox.showerror('Error', 'Invalid PNR')
                return
            cursor = connection.cursor()
            cursor.execute(f'select pid from ticket where pnr = "{pnr}"')
            found = cursor.fetchone()
            if found is None:
                messagebox.showerror("Error", "PNR Not found")
                return
            cursor = connection.cursor()
            cursor.execute(f"delete from ticket where pnr = '{pnr}'")
            connection.commit()
            messagebox.showinfo("Ticket Cancelled", f"Ticket with PNR {pnr} cancelled Successfully")
            self.updateWaiting()
            if userid != 0:
                self.optioner(userid)
            else:
                self.admin()

        self.delete(ALL)
        root.title("IRCTC | TICKET CANCELATION")
        self.create_image(0, 0, image = f1, anchor = 'nw')
        if userid != 0:
            backBtn = Button(text = "BACK", command = lambda: self.optioner(userid))
            backBtn.bind('<Enter>', hoverInRd)
            backBtn.bind('<Leave>', hoverOutRd)
            self.create_window(100, 100, window = backBtn)
        else:
            backBtn = Button(text = "BACK", command = self.admin)
            backBtn.bind('<Enter>', hoverInRd)
            backBtn.bind('<Leave>', hoverOutRd)
            self.create_window(100, 100, window = backBtn)
        self.create_text(750, 300, text = 'Enter the PNR Number of the ticket to be cancelled', font = myFontH)
        pnr = StringVar()
        epnr = Entry(textvariable = pnr, font = myFont)
        self.create_window(750, 400, window = epnr)
        sbt = Button(text = "Proceed", command = lambda:processDelete(pnr.get().strip()), font = myFont)
        sbt.bind('<Enter>', hoverInColG)
        sbt.bind('<Leave>', hoverOutCol)
        self.create_window(750, 500, window = sbt)

    def updateWaiting(self):
        cursor = connection.cursor()
        cursor.execute('select distinct trainno from train')
        trainnos = cursor.fetchall()
        for i in trainnos:
            trno = i[0]
            cursor = connection.cursor()
            cursor.execute(f'select distinct traveldate from ticket where trainno = "{trno}"')
            dates = cursor.fetchall()
            for j in dates:
                cursor = connection.cursor()
                cursor.execute(f'select * from ticket where trainno = "{trno}" and traveldate = "{str(j[0])}"')
                resTicket = cursor.fetchall()
                tempSeats = [seats[0]]
                for x in seats[1:]:
                    tempSeats.append(list(x))
                cursor = connection.cursor()
                if resTicket is not None:
                    for x in resTicket:
                        if x[9] == 'general' and tempSeats[0] > 0:
                            if x[7] == 0 and tempSeats[0] > 0:
                                cursor.execute(f'update ticket set confirmed = 1 where pnr = "{x[1]}"')
                            tempSeats[0] -= 1
                        elif x[9] == 'sleeper':
                            if x[10] == 'u' and tempSeats[1][0] > 0:
                                if x[7] == 0 and tempSeats[1][0] > 0:
                                    cursor.execute(f'update ticket set confirmed = 1 where pnr = "{x[1]}"')
                                tempSeats[1][0] -= 1
                            elif x[10] == 'm' and tempSeats[1][1] > 0:
                                if x[7] == 0 and tempSeats[1][1] > 0:
                                    cursor.execute(f'update ticket set confirmed = 1 where pnr = "{x[1]}"')
                                tempSeats[1][1] -= 1
                            elif tempSeats[1][2] > 0:
                                if x[7] == 0 and tempSeats[1][2] > 0:
                                    cursor.execute(f'update ticket set confirmed = 1 where pnr = "{x[1]}"')
                                tempSeats[1][2] -= 1
                        elif x[9] == 'ac1':
                            if x[10] == 'u' and tempSeats[2][0]:
                                if x[7] == 0 and tempSeats[2][0] > 0:
                                    cursor.execute(f'update ticket set confirmed = 1 where pnr = "{x[1]}"')
                                tempSeats[2][0] -= 1
                            elif tempSeats[2][1] > 0:
                                if x[7] == 0 and tempSeats[2][1] > 0:
                                    cursor.execute(f'update ticket set confirmed = 1 where pnr = "{x[1]}"')
                                tempSeats[2][1] -= 1
                        elif x[9] == 'ac2':
                            if x[10] == 'u' and tempSeats[3][0] > 0:
                                if x[7] == 0 and tempSeats[3][0] > 0:
                                    cursor.execute(f'update ticket set confirmed = 1 where pnr = "{x[1]}"')
                                tempSeats[3][0] -= 1
                            elif tempSeats[3][1] > 0:
                                if x[7] == 0 and tempSeats[3][1] > 0:
                                    cursor.execute(f'update ticket set confirmed = 1 where pnr = "{x[1]}"')
                                tempSeats[3][1] -= 1
                        else:
                            if x[10] == 'u' and tempSeats[4][0] > 0:
                                if x[7] == 0 and tempSeats[4][0] > 0:
                                    cursor.execute(f'update ticket set confirmed = 1 where pnr = "{x[1]}"') 
                                tempSeats[4][0] -= 1
                            elif x[10] == 'm' and tempSeats[4][1] > 0:
                                if x[7] == 0 and tempSeats[4][1] > 0:
                                    cursor.execute(f'update ticket set confirmed = 1 where pnr = "{x[1]}"')
                                tempSeats[4][1] -= 1
                            elif x[10] == 'l' and tempSeats[4][2] > 0:
                                if x[7] == 0 and tempSeats[4][2] > 0:
                                    cursor.execute(f'update ticket set confirmed = 1 where pnr = "{x[1]}"')
                                tempSeats[4][2] -= 1
                connection.commit()

init = Page()


root.mainloop()