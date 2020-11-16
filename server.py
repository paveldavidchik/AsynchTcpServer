import socket
import select


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 10001))
sock.listen(socket.SOMAXCONN)

conn1, addr1 = sock.accept()
conn2, addr2 = sock.accept()

conn1.setblocking(0)
conn2.setblocking(0)

epall = select.epoll()
epall.register(conn1.fileno(), select.EPOLLIN | select.EPOLLOUT)
epall.register(conn2.fileno(), select.EPOLLIN | select.EPOLLOUT)

conn_map = {
    conn1.fileno(): conn1,
    conn2.fileno(): conn2
}

while True:
    events = epall.poll()
    for fileno, event in events:
        if event & select.EPOLLIN:
            data = conn_map[fileno].recv(1024)
            print(data.decode('utf8'))
        elif event & select.EPOLLOUT:
            conn_map[fileno].send('ping'.encode('utf8'))