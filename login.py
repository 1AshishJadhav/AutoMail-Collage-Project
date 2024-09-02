from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Login")
root.geometry("950x500+300+200")
root.configure(background="#fff")
root.resizable(False, False)


img = PhotoImage(file='login_img.png')
Label(root, image=img, bg='white').place(x=50,y=50)

frame = Frame(root, width=350, height=350, bg='white')
frame.place(x=480, y=70)

heading = Label(frame, text='Sign In', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)


###############----------------------------------------------

user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
user.place(x=40, y=80)
user.insert(0, 'Username')

Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

#########-------------------------------------------------

code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
code.place(x=40, y=150)
code.insert(0, 'Password')

Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)


            
            
            
            
root.mainloop()