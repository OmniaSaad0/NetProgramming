import socket
import threading



def broadcast(m, sender=-1):
    for client in clients:
        if client != sender:
            packed_length = (str(len(m))+':').encode('utf-8')
            client.send(packed_length)
            client.send(m.encode('utf-8'))




def handle_clints(client):
    while True:
        try:
            temp = client.recv(5).decode('utf-8')

            length = 0
            m = ''

            for i in range(len(temp)) :
                if temp[i] == ':' :
                    length = int(temp[:i])
                    m = temp[i+1:]
                    break

            m += client.recv(length).decode('utf-8')

            for i in range(length):
                if m[i] == ':':
                    temp = m[i+2:]

            if temp == 'EXIT':
                exit(client)
                break

            broadcast(m ,client)
        except Exception as e :
            print(f'ERORRRR : {e}')
            exit(client)
            break



def exit(client):
    index = clients.index(client)
    clients.remove(client)
    # client.close()
    nickname = nicknames[index]
    broadcast(f'\n{nickname} left!')
    nicknames.remove(nickname)
    # client.close()


def add_visitors():
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send('NICKNAME'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        print('---------------------------------------')
        print(nickname)
        nicknames.append(nickname)
        clients.append(client)

        broadcast(f"\n{nickname} joined!")

        thread = threading.Thread(target=handle_clints, args=(client,))
        thread.start()



host = '127.0.0.1'
port = 7000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

clients = []
nicknames = []
add_visitors()
