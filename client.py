import os
import socket
import signal
import time
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect((HOST, PORT))
        pid = os.fork()
        if pid > 0:
            while True:
                inp = input()
                s.sendall(f'{inp}'.encode())

        else:
            while True:
                time.sleep(1)
                data = s.recv(1024)
                if data == b'exit':
                    break
                print(f"Received {data.decode()}")

            os.waitpid(pid, 0)
            pgid = os.getpgid(0)
            os.killpg(pgid, signal.SIGTERM)
finally:
    s.close()
