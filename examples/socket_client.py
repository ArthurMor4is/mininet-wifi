
import sys
import socket
import time

def loop_message(s):
    i = 0
    s.send(str('get.ap1.position').encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    print(data)
    while(True):
        s.send(str('get.ap1.position').encode('utf-8'))
        data = s.recv(1024).decode('utf-8')
        print(data)
        i += 1
        time.sleep(0.5)
        s.close()

def client():
    import socket
    HOST = '127.0.0.1'  # Endereco IP do Servidor
    PORT = 5000  # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)
    print('Para sair use CTRL+X\n')
    msg = raw_input()
    while (msg != '\x18'):
        tcp.send(msg)
        msg = raw_input()
    tcp.close()
    # host = '127.0.0.1'
    # port = 12345  # Make sure it's within the > 1024 $$ <65535 range
    # message = ''
    # while message != 'q' and message != 'exit':
    #     s = socket.socket()
    #     s.connect((host, port))
    #     if sys.version_info.major == 3:
    #         message = input('-> ')
    #     else:
    #         message = raw_input('-> ')
    # if message == 'TESTE':
    #     print('Chamei o teste')
    #     loop_message(s)
    # else:
    #     s.send(str(message).encode('utf-8'))
    #     data = s.recv(1024).decode('utf-8')
    #     print('Received from server: ' + data)
    # s.close()


if __name__ == '__main__':
    client()
