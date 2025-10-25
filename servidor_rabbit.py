import socket
import pika
from concurrent.futures import ThreadPoolExecutor

HOST = '127.0.0.1'
PORT = 5000
MAX_WORKERS = 3

# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='tareas')

def manejar_cliente(conn, addr):
    print(f"[NUEVA CONEXIÓN] {addr} conectado.")
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            print(f"[{addr}] Enviando tarea a RabbitMQ: {data}")
            channel.basic_publish(exchange='', routing_key='tareas', body=data)
            respuesta = f"Tarea '{data}' enviada a la cola de procesamiento."
            conn.send(respuesta.encode('utf-8'))

    except ConnectionResetError:
        pass
    finally:
        conn.close()
        print(f"[DESCONECTADO] {addr}")

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[ESCUCHANDO] Servidor en {HOST}:{PORT}")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        print(f"[POOL ACTIVO] Capacidad: {MAX_WORKERS} workers\n")
        while True:
            conn, addr = server.accept()
            executor.submit(manejar_cliente, conn, addr)

if __name__ == "__main__":
    print("[SERVIDOR RABBITMQ INICIADO...]")
    iniciar_servidor()
