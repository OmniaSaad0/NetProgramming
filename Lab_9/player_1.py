from tkinter import Tk, Button, ttk, StringVar, Label, messagebox
import socket
from TicTacToe import StartGame


def configration():
    global chois
    if chose_var.get() == 'X':
        chois = 1
    else:
        chois = 2


def ok(play_again_win, game):
    global turn
    client_socket.send(str("10").encode('utf-8'))
    while True:
        if game.move == 10:
            ans = 10
            break
        if game.move == 0:
            ans = 0
            break

    if ans == 10:
        play_again_win.destroy()
        turn = 1
        start_game()
    elif ans == 0:
        messagebox.showinfo("Game Over!", "The other player rejected the invitation...")
        play_again_win.destroy()


def quit_game(play_again_win):
    client_socket.send(str("0").encode('utf-8'))
    play_again_win.destroy()


def play_again(game):
    play_again_win = Tk()
    play_again_win.geometry("280x120")
    play_again_win.title('play again')
    play_again_win.resizable(False, False)

    play_again_label = Label(play_again_win, text='Do you want to play again ?', font=("Inter", 16 * -1))
    play_again_label .place(x=50, y=20)
    ok_button = Button(play_again_win, command=lambda: ok(play_again_win, game), text="OK")
    quit_button = Button(play_again_win, command=lambda: quit_game(play_again_win), text="Quit")
    ok_button.configure(padx=5, pady=20)
    ok_button.place(x=70, y=60, height=30, width=60)
    quit_button.configure(padx=5, pady=20)
    quit_button.place(x=150, y=60, height=30, width=60)
    play_again_win.mainloop()


def get_score(game, old_score):
    old_score = list(old_score)
    if game.winner == 'u':
        old_score[0] += 1
    elif game.winner == 'o':
        old_score[1] += 1

    old_score = tuple(old_score)
    return old_score


def start_game():
    global score
    game = StartGame(client_socket, chois, turn, score)
    score = get_score(game, score)
    play_again(game)


def connect():  # as a client
    global begin_win
    global client_socket
    configration()
    ip = '127.0.0.1'
    port = 10000
    client_socket.connect((ip, port))
    client_socket.send(str(chois).encode('utf-8'))
    begin_win.destroy()
    start_game()


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
turn = 0
chois = 0
score = (0, 0)
begin_win = Tk()
chose_var = StringVar()
begin_win.geometry("280x150")
begin_win.title('Start Game')
begin_win.resizable(False, False)

label = Label(begin_win, text='chose your Letter')
label.grid(row=1, column=1, padx=10, pady=20)
chose = ttk.Combobox(begin_win, textvariable=chose_var, values=['X', 'O'])
chose.grid(row=1, column=2, padx=10, pady=20)
connect_button = Button(begin_win, command=connect, text="Connect")
connect_button.configure(padx=5, pady=20)
connect_button.place(x=100, y=70, height=40, width=80)
begin_win.mainloop()
