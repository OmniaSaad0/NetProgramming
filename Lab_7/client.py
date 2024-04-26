from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button, messagebox
import socket
import threading


class GUI:
    client_socket = None
    last_received_message = None

    def __init__(self, master):
        self.root = master
        self.chat_area = None
        self.nickname_section = None
        self.enter_message_text = None
        self.join_button = None
        self.initialize_socket()
        self.initialize_gui()
        self.create_receive_thread()

    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'
        port = 7000
        self.client_socket.connect((host, port))

    def initialize_gui(self):
        self.root.title("Chat Room")
        self.root.resizable(0, 0)
        self.display_chat_box()
        self.display_name_section()
        self.display_chat_entry_box()

    def create_receive_thread(self):
        thread = threading.Thread(target=self.receive_message_from_server, args=(self.client_socket,))
        thread.start()

    def receive_message_from_server(self, so):
        while True:
            temp = so.recv(5)
            if not temp:
                break

            length, message = temp.decode('utf-8').split(':', 1)
            length = int(length)
            message += so.recv(length).decode('utf-8')

            if "joined" in message:
                message = message.split(":")[1]+ " has joined the room..."
                self.chat_area.insert('end', message + '\n')
                self.chat_area.yview(END)
            elif "leaving" in message:
                message = message.split(":")[1] + " has left the room..."
                self.chat_area.insert('end', message + '\n')
                self.chat_area.yview(END)
            else:
                message = message.strip()
                self.chat_area.insert('end', message + '\n')
                self.chat_area.yview(END)
        so.close()

    def display_name_section(self):
        frame = Frame()
        Label(frame, text='Enter your nickname:', font=("Helvetica", 16)).pack(side='left', padx=10)
        self.nickname_section = Entry(frame, width=50, borderwidth=2)
        self.nickname_section.pack(side='left', anchor='e')
        self.join_button = Button(frame, text="Join", width=10, command=self.join)
        self.join_button.pack(side='left', anchor='e')
        frame.pack(side='top', anchor='nw')

    def display_chat_box(self):
        frame = Frame()
        Label(frame, text='The Chat :', font=("Serif", 12)).pack(side='top', anchor='w')
        self.chat_area = Text(frame, width=60, height=10, font=("Serif", 12))
        scrollbar = Scrollbar(frame, command=self.chat_area.yview, orient=VERTICAL)
        self.chat_area.config(yscrollcommand=scrollbar.set)
        self.chat_area.bind('<KeyPress>', lambda e: 'break')
        self.chat_area.pack(side='left', padx=10)
        scrollbar.pack(side='right', fill='y')
        frame.pack(side='top')

    def display_chat_entry_box(self):
        frame = Frame()
        Label(frame, text='Enter message:', font=("Serif", 12)).pack(side='top', anchor='w')
        self.enter_message_text = Text(frame, width=60, height=3, font=("Serif", 12))
        self.enter_message_text.pack(side='left', pady=15)
        self.enter_message_text.bind('<Return>', self.enter_key_pressed)
        frame.pack(side='top')

    def join(self):
        if len(self.nickname_section.get()) == 0:
            messagebox.showerror("Enter your nickname", "Enter your nickname to send a message")
            return

        self.nickname_section.config(state='disabled')
        message = "joined:" + self.nickname_section.get()
        self.client_socket.send((str(len(message))+': ').encode('utf-8'))
        self.client_socket.send(message.encode('utf-8'))

    def leave(self):
        if len(self.nickname_section.get()) == 0:
            messagebox.showerror("Enter your nickname", "Enter your nickname to send a message")
            return

        self.nickname_section.config(state='disabled')
        message = "leaving:" + self.nickname_section.get()
        self.client_socket.send((str(len(message))+': ').encode('utf-8'))
        self.client_socket.send(message.encode('utf-8'))

    def enter_key_pressed(self, event):
        if len(self.nickname_section.get()) == 0:
            messagebox.showerror("Enter your nickname", "Enter your nickname to send a message")
            return

        self.send_chat()
        self.clear_text()

    def clear_text(self):
        self.enter_message_text.delete(1.0, 'end')

    def send_chat(self):
        senders_name = self.nickname_section.get().strip() + ": "
        data = self.enter_message_text.get(1.0, 'end').strip()
        message = (senders_name + data)
        self.chat_area.insert('end', message + '\n')
        self.chat_area.yview(END)
        self.client_socket.send((str(len(message))+': ').encode('utf-8'))
        self.client_socket.send(message.encode('utf-8'))

        return 'break'

    def close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.leave()
            self.root.destroy()
            self.client_socket.close()
            exit(0)


if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.close_window)
    root.mainloop()
