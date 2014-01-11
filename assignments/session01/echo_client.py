import socket
import sys


def client(msg, log_buffer=sys.stderr):
    server_address = ('localhost', 10000)
    # a TCP socket with IPv4 Addressing, call the socket you make 'sock'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print the address that client will connect to.
    print >>log_buffer, 'connecting to {0} port {1}'.format(*server_address)
    # connect the socket to the server address.
    sock.connect(server_address)
    # this try/finally block exists purely to allow us to close the socket on complete.
    try:
        print >>log_buffer, 'sending "{0}"'.format(msg)
        # send the message to the server.
        sock.send(msg)
        # the server sent message as a series of 16-byte chunks. Print each message, and wait until receiving
        # the entire message before closing the socket.
        message_return = ''
        while message_return != msg:
            chunk = sock.recv(16)
            if not chunk:
                break
            message_return += chunk
            print >>log_buffer, 'received "{0}"'.format(chunk)
    finally:
        #  close the client server after receiving the entire message.
        print >>log_buffer, 'closing socket'
        sock.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usg = '\nusage: python echo_client.py "this is my message"\n'
        print >>sys.stderr, usg
        sys.exit(1)
    
    msg = sys.argv[1]
    client(msg)