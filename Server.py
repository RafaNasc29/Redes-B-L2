import socket
import os
from tqdm import tqdm

IP = socket.gethostname()
PORT = 65435
ADDR = (IP, PORT)
SIZE = 1024
FILENAME = 'test.exe'
FILESIZE = os.path.getsize(FILENAME)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("Listening...")
    conn, addr = server.accept()
    print('Client connected')

    data = f"{FILENAME}_{FILESIZE}"
    conn.send(data.encode('utf-8'))
    bar = tqdm(range(FILESIZE), f'Receiving {FILENAME}', unit="B", unit_scale = True, unit_divisor = SIZE)

    with open(FILENAME, 'rb') as f:
        while True:
            data = f.read(SIZE)
            if not data:
                break
            conn.send(data)
            bar.update(len(data))
    conn.close()
    server.close()
if __name__ == '__main__':
    main()
