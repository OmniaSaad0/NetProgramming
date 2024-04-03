from socket import *
from math import ceil
s = socket(AF_INET, SOCK_STREAM)

host = '192.168.27.131'
port = 4000

try :
    s.connect((host,port))
    print('connected...')
    print('Enter EXIT to end chat ...')

    while True:

        m = input('You : ')
        s.send(str(len(m)).encode())
        total_sent = 0
        while total_sent < len(m):
            chunk = m[total_sent : total_sent + min(2048,len(m)-total_sent)]
            # print(chunk)
            sent = s.send(str(chunk).encode())
            total_sent += sent

        if m == 'EXIT':
            break

        length = int(s.recv(4).decode())
        m = ''
        total_recv = 0
        while total_recv < length:
            data = s.recv(2048).decode()
            # print('Typing...')
            m += data
            total_recv +=len(data)

        print('server : ',m)


    s.close()
except Exception as e :
    print(e)
