from tkinter import Tk, Canvas, Button, PhotoImage, messagebox
from threading import Thread


def make_button(fun, x_pos, y_pos, image, text='#', width=53.0, height=54.0):
    button = Button(image=image, text=text, borderwidth=0, highlightthickness=0,
                    bg="#FFFFFF", command=fun, relief="flat")
    button.place(x=x_pos, y=y_pos, width=width, height=height)
    return button


class StartGame:
    def __init__(self, so, chois, turn, score):
        print("Start turn : ", turn)
        self.move = -1
        self.winner = ""
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.window.geometry("328x226")
        self.canvas = Canvas(self.window, bg="#FFFFFF", height=226, width=328, bd=0, highlightthickness=0,
                             relief="ridge")
        self.button_image_1 = PhotoImage(file="button_1.png")
        self.button_image_2 = PhotoImage(file="button_2.png")
        self.button_image_3 = PhotoImage(file="button_3.png")
        self.button_image_4 = PhotoImage(file="button_6.png")
        self.button_image_5 = PhotoImage(file="button_9.png")
        self.canvas.place(x=0, y=0)
        self.turn = turn
        self.flag = 0
        self.button_1 = None
        self.button_2 = None
        self.button_3 = None
        self.button_4 = None
        self.button_5 = None
        self.button_6 = None
        self.button_7 = None
        self.button_8 = None
        self.button_9 = None
        self.your_img = None
        self.other_img = None
        self.your_letter = None
        self.other_letter = None
        self.player = so
        self.configu(chois)
        self.board = []
        self.creat_board(score)
        self.window.resizable(False, False)
        self.t = Thread(target=self.receive_move, args=(so,))
        self.t.start()
        self.window.mainloop()

    def configu(self, choise):
        if choise == 1:
            self.your_img = PhotoImage(file='x.png')
            self.other_img = PhotoImage(file='o.png')
            self.your_letter = 'X'
            self.other_letter = 'O'

        else:
            self.your_img = PhotoImage(file='o.png')
            self.other_img = PhotoImage(file='x.png')
            self.your_letter = 'O'
            self.other_letter = 'X'

    def handle_received_move(self, move):
        if self.turn == 1 and 0 < move < 10:
            self.move = move - 1
            self.board[self.move].config(image=self.other_img, text=self.other_letter)
            self.turn = 1 - self.turn
            self.check()

    def receive_move(self, player):
        while True:
            try:
                self.move = int(player.recv(4).decode('utf-8'))
                self.window.after(0, self.handle_received_move, self.move)
            except Exception:
                break

    def creat_board(self, score):
        self.button_1 = make_button(self.button_1_clicked, 136.0, 27.0, self.button_image_5)
        self.button_2 = make_button(self.button_2_clicked, 200.0, 27.0, self.button_image_3)
        self.button_3 = make_button(self.button_3_clicked, 260.0, 27.0, self.button_image_1)

        self.button_4 = make_button(self.button_4_clicked, 136.0, 86.0, self.button_image_3)
        self.button_5 = make_button(self.button_5_clicked, 200.0, 86.0, self.button_image_3)
        self.button_6 = make_button(self.button_6_clicked, 260.0, 86.0, self.button_image_3)

        self.button_7 = make_button(self.button_7_clicked, 136.0, 149.0, self.button_image_4)
        self.button_8 = make_button(self.button_8_clicked, 200.0, 149.0, self.button_image_3)
        self.button_9 = make_button(self.button_9_clicked, 260.0, 149.0, self.button_image_2)

        self.board.append(self.button_1)
        self.board.append(self.button_2)
        self.board.append(self.button_3)
        self.board.append(self.button_4)
        self.board.append(self.button_5)
        self.board.append(self.button_6)
        self.board.append(self.button_7)
        self.board.append(self.button_8)
        self.board.append(self.button_9)

        self.canvas.create_text(9.0, 91.0, anchor="nw", text="Score: \nYou : "+str(score[0])+"\nother : "+str(score[1]),
                                fill="#000000", font=("Inter", 12 * -1))

        self.canvas.create_text(5.0, 23.0, anchor="nw", text=("You Play with: "+self.your_letter), fill="#000000",
                                font=("Inter", 12 * -1))

    def button_1_clicked(self):
        if self.button_1["text"] == "#":
            if self.turn == 0:
                self.turn = 1 - self.turn
                self.button_1.config(image=self.your_img, text=self.your_letter)
                self.player.send(str("1").encode('utf-8'))
            self.check()

    def button_2_clicked(self):
        if self.button_2["text"] == "#":
            if self.turn == 0:
                self.turn = 1 - self.turn
                self.button_2.config(image=self.your_img, text=self.your_letter)
                self.player.send(str("2").encode('utf-8'))
            self.check()

    def button_3_clicked(self):
        if self.button_3["text"] == "#":
            if self.turn == 0:
                self.turn = 1 - self.turn
                self.button_3.config(image=self.your_img, text=self.your_letter)
                self.player.send(str("3").encode('utf-8'))
            self.check()

    def button_4_clicked(self):
        if self.button_4["text"] == "#":
            if self.turn == 0:
                self.turn = 1 - self.turn
                self.button_4.config(image=self.your_img, text=self.your_letter)
                self.player.send(str("4").encode('utf-8'))
            self.check()

    def button_5_clicked(self):
        if self.button_5["text"] == "#":
            if self.turn == 0:
                self.turn = 1 - self.turn
                self.button_5.config(image=self.your_img, text=self.your_letter)
                self.player.send(str("5").encode('utf-8'))
            self.check()

    def button_6_clicked(self):
        if self.button_6["text"] == "#":
            if self.turn == 0:
                self.turn = 1 - self.turn
                self.button_6.config(image=self.your_img, text=self.your_letter)
                self.player.send(str("6").encode('utf-8'))
            self.check()

    def button_7_clicked(self):
        if self.button_7["text"] == "#":
            if self.turn == 0:
                self.turn = 1 - self.turn
                self.button_7.config(image=self.your_img, text=self.your_letter)
                self.player.send(str("7").encode('utf-8'))
            self.check()

    def button_8_clicked(self):
        if self.button_8["text"] == "#":
            if self.turn == 0:
                self.turn = 1 - self.turn
                self.button_8.config(image=self.your_img, text=self.your_letter)
                self.player.send(str("8").encode('utf-8'))
            self.check()

    def button_9_clicked(self):
        if self.button_9["text"] == "#":
            if self.turn == 0:
                self.turn = 1 - self.turn
                self.button_9.config(image=self.your_img, text=self.your_letter)
                self.player.send(str("9").encode('utf-8'))
            self.check()

    def check(self):
        b1 = self.button_1["text"]
        b2 = self.button_2["text"]
        b3 = self.button_3["text"]
        b4 = self.button_4["text"]
        b5 = self.button_5["text"]
        b6 = self.button_6["text"]
        b7 = self.button_7["text"]
        b8 = self.button_8["text"]
        b9 = self.button_9["text"]

        self.flag = self.flag + 1
        if (b1 == b2 and b1 == b3 and b1 == self.other_letter) or (b1 == b2 and b1 == b3 and b1 == self.your_letter):
            self.win(self.button_1["text"])
        elif (b4 == b5 and b4 == b6 and b4 == self.other_letter) or (b4 == b5 and b4 == b6 and b4 == self.your_letter):
            self.win(self.button_4["text"])
        elif (b7 == b8 and b7 == b9 and b7 == self.other_letter) or (b7 == b8 and b7 == b9 and b7 == self.your_letter):
            self.win(self.button_7["text"])

        elif (b1 == b4 and b1 == b7 and b1 == self.other_letter) or (b1 == b4 and b1 == b7 and b1 == self.your_letter):
            self.win(self.button_1["text"])
        elif (b2 == b5 and b2 == b8 and b2 == self.other_letter) or (b2 == b5 and b2 == b8 and b2 == self.your_letter):
            self.win(self.button_2["text"])
        elif (b3 == b6 and b3 == b9 and b3 == self.other_letter) or (b3 == b6 and b3 == b9 and b3 == self.your_letter):
            self.win(self.button_3["text"])

        elif (b1 == b5 and b1 == b9 and b1 == self.other_letter) or (b1 == b5 and b1 == b9 and b1 == self.your_letter):
            self.win(self.button_1["text"])
        elif (b7 == b5 and b7 == b3 and b7 == self.other_letter) or (b7 == b5 and b7 == b3 and b7 == self.your_letter):
            self.win(self.button_7["text"])
        else:
            print("still no wining..")
            # print(b1, ' ', b2, ' ', b3)
            # print(b4, ' ', b5, ' ', b6)
            # print(b7, ' ', b8, ' ', b9)

        if self.flag == 10:
            messagebox.showinfo("Tie", "Match Tied!!!  Try again :)")
            self.winner = "tie"
            self.window.destroy()

    def win(self, player):
        ans = "Game complete "
        if player == self.your_letter:
            ans += "Your letter "+self.your_letter+" wins "
            self.winner = "u"
        else:
            ans += "Other player "+self.your_letter+" wins "
            self.winner = 'o'

        messagebox.showinfo("Game Over!", ans)
        self.window.destroy()
