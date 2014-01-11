import socket
import sys


def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 10000)
    # a TCP socket with IPv4 Addressing, call the socket you make 'sock'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # log that we are building a server
    print >>log_buffer, "making a server on {0}:{1}".format(*address)

    # for incoming connections
    sock.bind(address)
    sock.listen(1)
    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print >>log_buffer, 'waiting for a connection'
            # accept the client connection, get the socket connected and the address.
            connection, client_address = sock.accept()
            try:
                print >>log_buffer, 'connection - {0}:{1}'.format(*client_address)
                # the inner loop will receive messages sent by the client in 
                # buffers and exit when a complete message has been received.
                while True:
                    # receive 16 bytes of data from the client. Store the data you receive as 'data'.
                    data = connection.recv(16)
                    # if no data receive, exit the inner loop.
                    if not data:
                        break
                    print >>log_buffer, 'received "{0}"'.format(data)
                    connection.send(data)
            finally:
                # close the connection.
                connection.close()
    except KeyboardInterrupt:
        # close the server on key interrupt.
        sock.close()

if __name__ == '__main__':
    server()
    sys.exit(0)