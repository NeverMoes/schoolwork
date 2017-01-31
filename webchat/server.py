import socket
import select


def broadcast(sock, message):
    for socket in alive_pool:
        if socket != serv_sock and socket != sock:
            try:
                socket.send(message)
            except:
                socket.close()
                alive_pool.remove(socket)


if __name__ == '__main__':

    alive_pool = []
    BUF_SIZE = 4096
    ADDRESS = ('', 6666)

    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv_sock.bind(ADDRESS)
    serv_sock.listen(10)

    alive_pool.append(serv_sock)

    print("Chat server started on port: ", ADDRESS[1])

    while True:

        read_socks, write_socks, error_socks = select.select(alive_pool, [], [])

        for sock in read_socks:
            if sock == serv_sock:
                sockfd, addr = serv_sock.accept()
                alive_pool.append(sockfd)
                print("Client (%s, %s) connected" % addr)

                broadcast(sockfd, "[%s:%s] entered roomn" % addr)

            else:
                try:
                    data = sock.recv(BUF_SIZE)
                    if data:
                        broadcast(sock, "r" + ' ' + data)

                except:
                    broadcast(sock, "Client (%s, %s) is offline" % addr)
                    print("Client (%s, %s) is offline" % addr)
                    sock.close()
                    alive_pool.remove(sock)
                    continue

    serv_sock.close()