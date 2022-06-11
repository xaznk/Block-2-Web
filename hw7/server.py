import socket
import threading


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc.bind(("127.0.0.1", 1235))
soc.listen(5)


users = []


def send_all(data):
    for user in users:
        user.send(data)


def listen_user(user):
    while True:
        try:
            data = user.recv(4096)
            if data:
                print(f"User sent {data}")

                send_all(data)
            else:
                remove(user)
        except:
            continue


def start_server():
    while True:
        user_socket, addr = soc.accept()
        print(f"User with {addr}, connected")
        users.append(user_socket)

        listening_concurently = threading.Thread(
            target=listen_user, args=(user_socket,))
        listening_concurently.start()


if __name__ == "__main__":
    start_server()
