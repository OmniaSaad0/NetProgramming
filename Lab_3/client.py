import socket
import threading


def receive(client):
    while not close:
        try:
            temp = client.recv(5).decode('utf-8')
            length = 0
            m = ''
            for i in range(len(temp)):
                if temp[i] == ':' :
                    length = int(temp[:i])
                    m = temp[i+1:]
                    break

            m += client.recv(length).decode('utf-8')
            print(m)

        except Exception as e:
            # print(f'ERRRRORRRR : {e}')
            client.close()
            break



def send(client):
    while True:
        m = input()
        packed_length = (str(len(nickname)+3+len(m))+':').encode('utf-8')
        client.send(packed_length)
        client.send((f'{nickname} : {m}').encode('utf-8'))

        if m == 'EXIT':
            client.close()
            close = True
            break



##############################################################
close = False
nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 7000
client.connect((host, port))

message = client.recv(1024).decode('utf-8')
client.send(nickname.encode('utf-8'))

send_thread = threading.Thread(target=send ,args=(client,))
send_thread.start()

receive_thread = threading.Thread(target=receive ,args=(client,))
receive_thread.start()

send_thread.join()
receive_thread.join()
