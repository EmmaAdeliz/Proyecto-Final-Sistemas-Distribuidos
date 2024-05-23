import socket
import threading
import os

def handle_client(connection, address, connections):
    print(f"Conexión establecida desde {address}")
    
    try:
        # Enviar mensaje de bienvenida al cliente
        welcome_message = "Conexión establecida. Envíe su archivo."
        connection.sendall(welcome_message.encode('utf-8'))
        print("Mensaje de bienvenida enviado al cliente.")
        
        # Recibir datos del archivo en bloques de 1024 bytes
        end_marker = b'EOF'  # Marcador especial para indicar el fin del archivo
        filename = f'received_file_from_{address[0]}.bin'
        with open(filename, 'wb') as f:
            while True:
                data = connection.recv(1024)
                if end_marker in data:
                    data = data.replace(end_marker, b'')
                    if data:
                        f.write(data)
                    break
                f.write(data)
        print(f"Archivo recibido de {address}")

        # Reproducir el archivo si es música y si existe
        if filename.lower().endswith(('.mp3', '.wav', '.ogg')) and os.path.exists(filename):
            print("Reproduciendo archivo de música...")
            try:
                os.startfile(filename)  # Abre el archivo con el programa predeterminado de Windows
            except Exception as e:
                print(f"No se pudo abrir el archivo: {e}")

        # Enviar confirmación al cliente
        confirmation_message = "Archivo recibido con éxito."
        connection.sendall(confirmation_message.encode('utf-8'))
        print("Confirmación enviada al cliente.")

    except Exception as e:
        print(f"Error al recibir datos de {address}: {e}")
    
    print(f"Conexión cerrada desde {address}")
    connection.close()
    del connections[address]

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('192.168.43.137', 8080))
        server_socket.listen(3)
        print("Servidor iniciado en 192.168.43.137:8080")
    except Exception as e:
        print(f"Error al intentar bind en el puerto: {e}")
        return
    

    connections = {}

    while True:
        print("Esperando nuevas conexiones...")
        connection, address = server_socket.accept()
        print(f"Nueva conexión aceptada de {address}")
        connections[address] = connection
        threading.Thread(target=handle_client, args=(connection, address, connections)).start()

if __name__ == "__main__":
    server()

