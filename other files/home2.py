from tkinter import *
from tkinter import messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from db import get_db

# Initialize the main window
root = Tk()
root.title("Login")
root.geometry("950x500+300+200")
root.configure(background="#fff")
root.resizable(False, False)

# Load images for login and signup
img = PhotoImage(file='images/login_img.png')
Label(root, image=img, bg='white').place(x=50,y=50)

img = PhotoImage(file='images/signup_img.png')
Label(root, image = img, border=0).place(x=20,y=90)


# Functions for handling user input
def on_enter(e, entry, placeholder):
    entry.delete(0, 'end')
    entry.config(fg='black')

def on_leave(e, entry, placeholder):
    if entry.get() == '':
        entry.insert(0, placeholder)
        entry.config(fg='gray')

# Function to handle login process
def signin():
    username = user.get()
    password = code.get()
    db = get_db()
    user_record = db.find_one({"username": username})
    if user_record and user_record.get('password') == password:
        show_main_content()
    else:
        messagebox.showerror('Invalid', 'Invalid username or password')



# Function to clear widgets and show the main content (p2 functionality)
def show_main_content():
    for widget in root.winfo_children():
        widget.destroy()


    window = TkinterDnD.Tk()  # Drag and drop functionality
    window.title("SignUp")
    window.geometry('925x500+300+200')
    window.configure(bg="#fff")
    window.resizable(False, False)

    # Callback function to handle dropped files
    def handle_drop(event):
        file_path = event.data
        if file_path.endswith('.xls') or file_path.endswith('.xlsx'):
            messagebox.showinfo("File Accepted", f"Excel sheet '{file_path}' has been uploaded successfully.")

            # Load the Excel file and populate the comboboxes
            global df  # Make the dataframe accessible globally
            df = pd.read_excel(file_path)
            columns = df.columns.tolist()

            name_selection['values'] = columns
            attendance_selection['values'] = columns
            email_selection['values'] = columns

            # Clear previous selections
            name_selection.set('')
            attendance_selection.set('')
            email_selection.set('')
        else:
            messagebox.showwarning("Invalid File", "Only Excel files (.xls, .xlsx) are allowed.")

    # This is the file panel that takes the Excel file
    box_frame = Frame(window, relief="solid", bd=1, bg="#fff", width=300, height=200)
    box_frame.grid(row=0, column=0, rowspan=2, padx=90, pady=30)
    box_label = Label(box_frame, text="Drag and Drop Excel Sheet Here", width=40, height=15, relief="solid", bg="#fff")
    box_label.pack()

    # Bind the drag and drop event to the box_frame
    box_frame.drop_target_register(DND_FILES)
    box_frame.dnd_bind('<<Drop>>', handle_drop)

    frame = Frame(window, bg='#fff')
    frame.place(x=480, y=50, width=350, height=390)

    # Labels and Comboboxes for column selection
    name_label = Label(frame, text="Select the name column:")
    name_label.pack(pady=(10, 0))
    name_selection = ttk.Combobox(frame, width=50)
    name_selection.pack(pady=(0, 10))

    attendance_label = Label(frame, text="Select the attendance column:")
    attendance_label.pack(pady=(10, 0))
    attendance_selection = ttk.Combobox(frame, width=50)
    attendance_selection.pack(pady=(0, 10))

    email_label = Label(frame, text="Select the email column:")
    email_label.pack(pady=(10, 0))
    email_selection = ttk.Combobox(frame, width=50)
    email_selection.pack(pady=(0, 10))

    # Text box for attendance criteria
    text_2_placeholder = "Enter the attendance criteria"
    text_2 = Text(frame, height=3, width=45, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
    text_2.pack(pady=(10, 0))
    text_2.insert("1.0", text_2_placeholder)
    text_2.config(fg='gray')

    # Function to send email
    def send_email(to_email, subject, message_body):
        try:
            # Email configuration
            sender_email = "your_email@example.com"  # Use your email
            sender_password = "your_password"  # Use your email password

            # Create MIME message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message_body, 'plain'))

            # Connect to server and send email
            server = smtplib.SMTP('smtp.gmail.com', 587)  # For Gmail
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            server.quit()

            print(f"Email sent to {to_email}")

        except Exception as e:
            print(f"Error sending email to {to_email}: {e}")

    # Function to process the selections and send emails
    def process_selection():
        name_col = name_selection.get()
        attendance_col = attendance_selection.get()
        email_col = email_selection.get()
        attendance_criteria = text_2.get("1.0", END).strip()
        additional_info = text_box_left.get("1.0", END).strip()

        if name_col and attendance_col and email_col and attendance_criteria:
            try:
                attendance_criteria = float(attendance_criteria)
                students_below_criteria = df[df[attendance_col] < attendance_criteria]
                if students_below_criteria.empty:
                    messagebox.showinfo("Information", "All students meet the attendance criteria.")
                else:
                    for _, row in students_below_criteria.iterrows():
                        student_name = row[name_col]
                        student_email = row[email_col]
                        email_body = f"Dear {student_name},\n\n{additional_info}"

                        send_email(student_email, "Attendance Warning", email_body)
                    messagebox.showinfo("Success", f"Emails sent to {len(students_below_criteria)} students.")
            except ValueError:
                messagebox.showerror("Error", "Invalid attendance criteria. Please enter a valid number.")
        else:
            messagebox.showwarning("Warning", "Please select all three columns and provide attendance criteria.")

    # Button to submit the selection
    Button(frame, width=45, pady=10, text='Submit', bg='#57a1f8', fg='white', border=0, command=process_selection).pack(pady=(20, 0))

    # Text box for additional information or instructions
    text_frame_left = Frame(window, relief="solid", bd=1)
    text_frame_left.grid(row=2, column=0, padx=20, pady=20)

    text_box_left = Text(text_frame_left, height=10, width=50, font=('Microsoft Yahei UI Light', 8))
    text_box_left.pack()

    # Start the TkinterDnD main loop
    window.mainloop()

# Function to show signup frame
def show_signup_frame():
    for widget in root.winfo_children():
        widget.destroy()



    signup_frame = Frame(root, width=950, height=500, bg='#fff')
    signup_frame.pack(fill='both', expand=True)

    def signup():
        username = user.get()
        password = code.get()
        conform_password = conform_code.get()
        if password == conform_password:
            db = get_db()
            if db.find_one({"username": username}):
                messagebox.showerror('Invalid', 'Username already exists')
            else:
                db.insert_one({"username": username, "password": password})
                messagebox.showinfo('Signup', 'Successfully signed up')
                show_login_frame()
        else:
            messagebox.showerror('Invalid', "Both Passwords should match")

    Label(signup_frame, border=0, bg='white').place(x=5, y=90)
    frame = Frame(signup_frame, width=500, height=390, bg='#fff')
    frame.place(x=400, y=50)

    

    heading = Label(frame, text="Sign Up", fg='#57a1f8', bg='white', font=('Microsoft Yahei UI Light', 23, 'bold'))
    heading.place(x=200, y=5)

    global user, code, conform_code
    user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
    user.place(x=130, y=80)
    user.insert(0, 'Username')
    user.bind("<FocusIn>", lambda e: on_enter(e, user, 'Username'))
    user.bind("<FocusOut>", lambda e: on_leave(e, user, 'Username'))

    Frame(frame, width=295, height=2, bg='black').place(x=130, y=110)

    code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
    code.place(x=130, y=130)
    code.insert(0, 'Password')
    code.bind("<FocusIn>", lambda e: on_enter(e, code, 'Password'))
    code.bind("<FocusOut>", lambda e: on_leave(e, code, 'Password'))

    Frame(frame, width=295, height=2, bg='black').place(x=130, y=160)

    conform_code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
    conform_code.place(x=130, y=180)
    conform_code.insert(0, 'Confirm Password')
    conform_code.bind("<FocusIn>", lambda e: on_enter(e, conform_code, 'Confirm Password'))
    conform_code.bind("<FocusOut>", lambda e: on_leave(e, conform_code, 'Confirm Password'))

    Frame(frame, width=295, height=2, bg='black').place(x=130, y=210)

    Button(frame,width=39,pady=5,text='Sign up',bg='#57a1f8', fg='white', border=0,command=signup).place(x=130,y=280)


# Function to show login frame
def show_login_frame():
    for widget in root.winfo_children():
        widget.destroy()

    login_frame = Frame(root, width=950, height=500, bg='#fff')
    login_frame.pack(fill='both', expand=True)

    heading = Label(login_frame, text='Sign In', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x=600, y=60)


    global user, code
    user = Entry(login_frame, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
    user.place(x=500, y=160)
    user.insert(0, 'Username')
    user.bind("<FocusIn>", lambda e: on_enter(e, user, 'Username'))
    user.bind("<FocusOut>", lambda e: on_leave(e, user, 'Username'))

    Frame(login_frame, width=295, height=2, bg='black').place(x=500, y=190)

    code = Entry(login_frame, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
    code.place(x=500, y=220)
    code.insert(0, 'Password')
    code.bind("<FocusIn>", lambda e: on_enter(e, code, 'Password'))
    code.bind("<FocusOut>", lambda e: on_leave(e, code, 'Password'))

    Frame(login_frame, width=295, height=2, bg='black').place(x=500, y=250)

    Button(login_frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0, command=signin).place(x=500, y=280)
    Button(login_frame,width=39,pady=7,text='Sign up',bg='#57a1f8', fg='white', border=0,command=show_signup_frame).place(x=500,y=320)

# Start the application by showing the login frame
show_login_frame()
root.mainloop()