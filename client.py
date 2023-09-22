import socket
from tqdm import tqdm
IP = socket.gethostname()
PORT = 65435
ADDR = (IP, PORT)
SIZE = 1024

def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(ADDR)
    data = conn.recv(SIZE).decode('utf-8')
    item = data.split('_')
    FILENAME = item[0]
    FILESIZE = int(item[1])

    bar = tqdm(range(FILESIZE), f'Receiving {FILENAME}', unit="B", unit_scale = True, unit_divisor = SIZE)
    with open(f"recv_{FILENAME}", "wb") as f:
        while True:
            data = conn.recv(SIZE)
            if not data:
                break
            f.write(data)
            bar.update(len(data))
    conn.close()

if __name__ == "__main__":
    main()
