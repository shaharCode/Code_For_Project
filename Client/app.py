import tkinter
from tkinter import *
from Client import Client
import threading
import socket
from tkinter import messagebox


# Checking if ip is valid
def is_valid_ip(ip: str) -> bool:
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

# trying to create a connection to the server through thread
# handling validity of ip by sending it to the func 'is_valid_ip'
global client
def creating_thread(ip):
    global client
    server_ip = ip
    if not is_valid_ip(ip):
        messagebox.showerror("Invalid IP Address",f"{ip} is not a valid IP address. Please enter a valid IP address.")
        return "invalid"
    server_port = 4444
    client = Client(server_ip, server_port)
    th = threading.Thread(target=client.connect_to_server())
    th.start()
    return client.connection_status


# Creating the Page to set the server ip
# Entering an ip address
app = Tk()
app.title("Vulnerability Scanner")
app.geometry("500x500")
app.resizable(False,False)

label = Label(app, text="Enter server ip",font=('Arial Bold',28))
label.grid(column=4 , row=0)
Entry = tkinter.Entry(app, width=20)
Entry.insert(0,socket.gethostbyname(socket.gethostname()))
Entry.focus()
Entry.grid(column=4 , row=4)

# instance of a click on the button
# sending entered ip to 'creating_thread' and proceeding according to the given result
def clicked():
    flag = creating_thread(Entry.get())
    if not flag == "invalid":
        if not flag:
            label2 = Label(app, text="Couldn't connect to server using this ip \n Enter a different one", font=('Arial Bold', 16))
            label2.grid(column=4, row=5)
        else:
            app.destroy()

Btn = Button(app, text="Set IP",command=clicked)
Btn.grid(column=4 , row=10)

app.mainloop()


# Sending the server a vulnerability type to scan
# Receiving the result of the scan from the server
def Send_To_Scan(type):
    global client
    client.send_data(type)
    result = client.recv_enc()

    return result


# Creating main Page
# Sending Vulnerability type, Receiving Scan result and displaying it
app = Tk()
app.title("Vulnerability Scanner")
app.geometry("500x500")
app.resizable(False,False)


label1 = Label(app, text="Enter Vulnerability to test",font=('Arial Bold',28))
label1.grid(column=1 , row=0)
Entry = tkinter.Entry(app, width=10)
Entry.focus()
Entry.grid(column=1 , row=4)


# instance of a click on the button
# sending entered data and receiving display result from 'Send_To_Scan'
def clicked():
    messageWindow.delete(1.0, END)
    value = Send_To_Scan(Entry.get())
    messageWindow.insert(END,value)
Btn = Button(app, text="Run",command=clicked)
Btn.grid(column=1 , row=5)

messageWindow = Text(app ,width=60, height=10)
messageWindow.grid(column=1 , row=6)

app.mainloop()
