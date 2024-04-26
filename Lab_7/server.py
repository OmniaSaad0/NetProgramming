import socket
import threading


def broadcast(m, sender=-1):
    for client in clients:
        if client != sender:
            client.send((str(len(m))+': ').encode('utf-8'))
            client.send(m.encode('utf-8'))


def receive_from_clients(client):
    while True:
        try:
            temp = client.recv(5).decode('utf-8')
            length, m = temp.split(':', 1)
            length = int(length)
            m += client.recv(length).decode('utf-8')

            if 'leaving' in m:
                exit_chat(client)

            broadcast(m, client)

        except Exception as e :
            print(f'ERORRRR : {e}')
            break


def exit_chat(client):
    clients.remove(client)
    client.close()


def add_clients():
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")
        clients.append(client)
        thread = threading.Thread(target=receive_from_clients, args=(client,))
        thread.start()


##########################################
host = '127.0.0.1'
port = 7000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)
print('server is listening to incoming requests...')
clients = []
add_clients()
