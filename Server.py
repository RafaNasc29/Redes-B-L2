# Igor Shinji Itiroko 20063301
# Marcelo Jurandir Marçura 20086898
# Gabriel Mateus Rosa 20057642
# Rafael Nascimento 20015558
import socket  # Importa o socket
import multiprocessing
import _thread
import time
HOST = "127.0.0.1"  # Endereço IP do host
PORT = 65432  # Porta a ser escutada
# echo-server.py
# vincula com uma conexão pre-estabelecida e passa a ouvir seu conteúdo
sharedMemories = {}
# Função que manda os valores para os clientes a partir do recebimento de parametro
def send_values(conn, addr):
    count = 0
    shm = sharedMemories[addr]
    while True:
        if shm.value.decode() == "exit":
            time.sleep(2)
            conn.sendto(b'exit', addr)
            for i in range(len (shm)):
                shm[i] = b'\x00'
            conn.close()
            break
        elif any(c != b'\x00' for c in shm):
            time.sleep(2)
            conn.sendto(f'{shm.value.decode()!r}'.encode('utf-8'), addr)
            for i in range(len (shm)):
                shm[i] = b'\x00'
        else:
            time.sleep(2)
            conn.sendto(bytes(f'{count}', 'utf-8'), addr)
            count += 1

# Função para o recebimento dos valores que os clientes mandam
def receive_values(conn, addr):
    shm = sharedMemories[addr]
    while True:
        data = conn.recv(1024)
        for i in range(len(data)):
            shm[i] = data[i]
        if shm.value.decode() == "exit":
            break

# Definindo um limite para o socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    limit = 3
    s.listen(limit)
    connections = 0
    while True:
        if connections == limit:
            continue
        conn, addr = s.accept()
        sharedMemories[addr] = multiprocessing.Array('c' , 10)
        print(f'Conectado em {addr}')
        connections += 1
        _thread.start_new_thread(receive_values, (conn, addr))
        _thread.start_new_thread(send_values, (conn, addr))
