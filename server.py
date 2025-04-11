import socket
import threading

# Server settings
HOST = '0.0.0.0'
PORT = 5000

clients = []
clients_lock = threading.Lock()

def broadcast(message, sender_conn):
    with clients_lock:
        for client in clients:
            if client != sender_conn:
                try:
                    client.sendall(message)
                except:
                    clients.remove(client)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    with conn:
        with clients_lock:
            clients.append(conn)

        while True:
            try:
                message = conn.recv(1024)
                if not message:
                    break
                broadcast(message, conn)
            except:
                break

        with clients_lock:
            if conn in clients:
                clients.remove(conn)
        print(f"[DISCONNECTED] {addr} disconnected.")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[LISTENING] Server is running on {HOST}:{PORT}")
        
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()

if __name__ == "__main__":
    main()
