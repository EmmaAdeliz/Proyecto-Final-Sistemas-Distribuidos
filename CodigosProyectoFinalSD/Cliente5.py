import socket
import os
import subprocess

def main():
    server_ip = '192.168.43.137'
    server_port = 8080
    end_marker = b'EOF'  # Marcador especial para indicar el fin del archivo

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
        print("Conexión establecida con el servidor.")
    except Exception as e:
        print(f"No se pudo conectar al servidor: {e}")
        return

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print("Mensaje recibido:", message)

            # Subir un archivo
            filename = input("Ingrese la ruta del archivo a enviar (o 'exit' para salir): ")
            if filename.lower() == 'exit':
                break

            with open(filename, 'rb') as f:
                file_data = f.read()
                client_socket.sendall(file_data)
                client_socket.sendall(end_marker)  # Enviar el marcador especial
                print("Archivo enviado con éxito.")

            # Reproducir el archivo si es música
            if filename.lower().endswith(('.mp3', '.wav', '.ogg')):
                print("Reproduciendo archivo de música...")
                subprocess.Popen(['xdg-open', filename])  # Abre el archivo en el reproductor predeterminado

        except ConnectionError as e:
            print(f"Error de conexión: {e}.")
            break
        except Exception as e:
            print(f"Error inesperado: {e}")
            break

    client_socket.close()

if __name__ == "__main__":
    main()
