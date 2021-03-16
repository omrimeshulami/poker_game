import socket
import threading
import Table
from Enums import TableStatus

# GLOBAL PARAMS


# GAME CONFIGURATION
STARTING_CASH = 1000
MINIMUM_NUMBER_OF_PLAYERS = 2
MAXIMUM_NUMBER_OF_PLAYERS = 5
SMALL_BLIND_VALUE = 5
BIG_BLIND_VALUE = 10

# socket configuration
tcp_port = 12345
ip_address = '127.0.0.1'
message_len = 1024
# GAME CONFIGURATION
table = None
thread_count = 0
players_ready = 0
players_limit = MAXIMUM_NUMBER_OF_PLAYERS
players = {}
table_status = TableStatus.NOT_READY

# lock for shared variables
lock = threading.Lock()


class TcpThread(threading.Thread):

    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket

    def run(self):
        global players_ready
        self.client_socket.send('Please enter your name name: '.encode('utf-8'))
        name = self.client_socket.recv(message_len).decode('utf-8')
        table.register_player(name)
        lock.acquire()
        players_ready += 1
        lock.release()
        self.client_socket.send(f'Waiting for {MINIMUM_NUMBER_OF_PLAYERS - players_ready} players...'.encode('utf-8'))
        while table_status == TableStatus.NOT_READY:
            continue
        while True:
            game_status = table.print_table_status()
            player_hand = table.get_player_hand(name)
            game_status += f'Your Hand:  {player_hand.first},{player_hand.second}'
            if table.current_player_name == name:
                game_status += "ITS YOUR TURN NOW"
            else:
                game_status += "ITS NOT YOUR TURN NOW"
            self.client_socket.send(game_status.encode('utf-8'))
            while table.current_player_name != name:
                pass
            self.client_socket.send(game_status.encode('utf-8'))

            data = self.client_socket.recv(message_len).decode('utf-8')
            table.player_action(data, name)
            # send_tcp_message(message, self.client_socket)
            self.client_socket.close()


def send_tcp_message(message, tcp_socket):
    lock.acquire()
    tcp_socket.send(message.encode('utf-8'))
    lock.release()


if __name__ == '__main__':
    while True:
        print("Server started,listening on localhost")
        server_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket_tcp.bind((ip_address, tcp_port))
        print('TCP socket wait for connection')
        server_socket_tcp.listen(4)
        table = Table.Table(SMALL_BLIND_VALUE, BIG_BLIND_VALUE)
        while True:
            if thread_count != players_limit:
                client_socket, addr = server_socket_tcp.accept()
                tcp = TcpThread(client_socket)
                tcp.start()
                lock.acquire()
                thread_count += 1
                lock.release()

            if 2 <= players_ready <= players_limit:
                table = Table.Table(SMALL_BLIND_VALUE, BIG_BLIND_VALUE, STARTING_CASH)
                table_status = TableStatus.READY
                break
