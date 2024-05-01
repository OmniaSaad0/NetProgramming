import socket
from tkinter import Tk, Label, Button
from TicTacToe import StartGame


def configration(other):
    global chois
    if other == 2:
        chois = 1
    else:
        chois = 2


def get_score(game, old_score):
    old_score = list(old_score)
    if game.winner == 'u':
        old_score[0] += 1
    elif game.winner == 'o':
        old_score[1] += 1

    old_score = tuple(old_score)
    return old_score


def ok(play_again_win):
    other_player.send("10".encode('utf-8'))
    print("new Game...")
    play_again_win.destroy()
    start_game()


def quit_game(play_again_win):
    other_player.send(str("0").encode('utf-8'))
    play_again_win.destroy()


def play_again():
    play_again_win = Tk()
    play_again_win.geometry("280x120")
    play_again_win.title('play again')
    play_again_win.resizable(False, False)

    play_again_label = Label(play_again_win, text='Do you want to play again ?', font=("Inter", 16 * -1))
    play_again_label .place(x=50, y=20)
    ok_button = Button(play_again_win, command=lambda: ok(play_again_win), text="OK")
    quit_button = Button(play_again_win, command=lambda: quit_game(play_again_win), text="Quit")
    ok_button.configure(padx=5, pady=20)
    ok_button.place(x=70, y=60, height=30, width=60)
    quit_button.configure(padx=5, pady=20)
    quit_button.place(x=150, y=60, height=30, width=60)
    play_again_win.mainloop()


def start_game():
    global turn
    global score
    global other_player
    game = StartGame(other_player, chois,turn, score)
    score = get_score(game, score)
    while True:
        if game.move == 10:
            ans = 10
            break
        if game.move == 0:
            ans = 0
            break
    if ans == 10:
        turn = 0
        play_again()
    elif ans == 0:
        other_player.close()


def listen():  # as a server
    global server_socket
    global other_player
    global add
    ip = '127.0.0.1'
    port = 10000
    server_socket.bind((ip, port))
    server_socket.listen(5)
    other_player, add = server_socket.accept()
    print("connected to ", add)
    other_chois = int(other_player.recv(5).decode('utf-8'))
    configration(other_chois)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
other_player = None
add = None
turn = 1
chois = 0
score = (0, 0)
listen()
start_game()
server_socket.close()
print("i'm back")
