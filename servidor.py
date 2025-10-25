import socket
import threading

# Configuración del servidor
HOST = '127.0.0.1'   # localhost
PORT = 5000          # puerto de escucha

def manejar_cliente(conn, addr):
    print(f"[NUEVA CONEXIÓN] {addr} conectado.")
    while True:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"[{addr}] Mensaje recibido: {data}")

            # Procesar la tarea 
            resultado = f"Resultado de '{data.upper()}'"
            conn.send(resultado.encode('utf-8'))

        except ConnectionResetError:
            break

    conn.close()
    print(f"[DESCONECTADO] {addr}")

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[ESCUCHANDO] Servidor en {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.start()
        print(f"[CONEXIONES ACTIVAS] {threading.active_count() - 1}")

if __name__ == "__main__":
    print("[INICIANDO SERVIDOR...]")
    iniciar_servidor()
