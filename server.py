from socket import *

s = socket(AF_INET, SOCK_STREAM)

host = '0.0.0.0'
port = 4000

s.bind((host,port))
print('binded successfully')

s.listen(5)
print('server is listenning ')

try:
    c, addr = s.accept()
    print('connection accepted from : ',addr)

    while True:

        length = int(c.recv(4)).decode()
        m = ''
        total_recv = 0
        while total_recv < length :
            data = c.recv(2048).decode()
            m += data
            total_recv += len(data)

        if m == 'EXIT':
            c.close()
            break

        print('clint :', m)

        m = input('You : ')
        c.send((str(len(m)).encode()))
        total_send = 0
        while total_send <len(m):
            chunk = m[total_send : total_send + min(2048 , len(m) - total_send)]
            sent = c.send(str(chunk).encode())
            total_send +=sent


    s.close()

except Exception as e:
    print('the connection didn\'t accepted due to : ' ,e)