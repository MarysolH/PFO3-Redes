import socket

# Configuración: debe coincidir con el servidor
HOST = '127.0.0.1'
PORT = 5000

def cliente():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Conectado al servidor en {HOST}:{PORT}")

        while True:
            mensaje = input("Ingrese una tarea (o 'salir' para terminar): ")
            if mensaje.lower() == 'salir':
                print("Cerrando conexión...")
                break

            # Enviar tarea al servidor
            s.sendall(mensaje.encode('utf-8'))

            # Esperar respuesta
            data = s.recv(1024).decode('utf-8')
            print(f"Respuesta del servidor: {data}")

if __name__ == "__main__":
    cliente()
