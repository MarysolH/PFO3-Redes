import socket
from concurrent.futures import ThreadPoolExecutor

# Configuración del servidor
HOST = '127.0.0.1'
PORT = 5000
MAX_WORKERS = 5   # Tamaño del pool de hilos (se ajustar este valor)

def manejar_cliente(conn, addr):
    print(f"[NUEVA CONEXIÓN] {addr} conectado.")
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            print(f"[{addr}] Tarea recibida: {data}")

            # Procesar la tarea (simulamos trabajo)
            resultado = f"Resultado procesado por worker: '{data.upper()}'"
            conn.send(resultado.encode('utf-8'))

    except ConnectionResetError:
        pass
    finally:
        conn.close()
        print(f"[DESCONECTADO] {addr}")

def iniciar_servidor():
    # Crear socket TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[ESCUCHANDO] Servidor en {HOST}:{PORT}")

    # Crear pool de hilos
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        print(f"[POOL ACTIVO] Capacidad: {MAX_WORKERS} workers\n")

        while True:
            conn, addr = server.accept()
            # Asignar la conexión a un hilo del pool
            executor.submit(manejar_cliente, conn, addr)

if __name__ == "__main__":
    print("[INICIANDO SERVIDOR CON POOL DE HILOS...]")
    iniciar_servidor()
