import socket
import threading

def find_index(item):
    index = -1
    for i in range(len(nicknames)):
        if nicknames[i] == item.strip():
            index = i
            break
    return index


def broadcast(m, sender=-1):
    for client in clients:
        if client != sender:
            packed_length = (str(len(m))+':').encode('utf-8')
            client.send(packed_length)
            client.send(m.encode('utf-8'))


def traverse(m, sender, recever):
    print(sender)
    print(recever)
    sender_index = find_index(sender)
    recever_index = find_index(recever)
    if recever_index != -1 :
        packed_length = (str(len(sender)+3+len(m))+':').encode('utf-8')
        clients[recever_index].send(packed_length)
        clients[recever_index].send((f'{sender} : {m}').encode('utf-8'))
    else :
        m = 'Server : This User is Not Connected in this time'
        packed_length = (str(len(m)) + ':').encode('utf-8')
        clients[sender_index].send(packed_length)
        clients[sender_index].send(m.encode('utf-8'))




def handle_clints(client):
    while True:
        try:
            temp = client.recv(5).decode('utf-8')

            length , m = temp.split(':',1)
            length = int(length)

            m += client.recv(length).decode('utf-8')
            # print('\n',m)
            recever ,sender , m = m.split(':' ,2)

            if m == 'EXIT':
                exit(client)
                break

            traverse(m ,sender , recever)

        except Exception as e :
            # print(f'ERORRRR : {e}')
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

        broadcast(f"\n{nickname} joined!",client)

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
