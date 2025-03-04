import socket
import threading
import socks

# Konfigurasi proxy SOCKS5 dengan autentikasi
PROXY_IP = "72.46.87.169"
PROXY_PORT = 80
PROXY_USER = "yljwouzu-rotate"  # Ganti dengan username proxy
PROXY_PASS = "xjm9z4vt0t2a"  # Ganti dengan password proxy

# Pool mining tujuan
POOL_HOST = "us.vipor.net"
POOL_PORT = 5040

# Set proxy dengan autentikasi
socks.set_default_proxy(socks.SOCKS5, PROXY_IP, PROXY_PORT, True, PROXY_USER, PROXY_PASS)
socket.socket = socks.socksocket

def handle_connection(client_socket, pool_socket):
    """ Meneruskan data antara miner <-> pool """
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            pool_socket.sendall(data)

            response = pool_socket.recv(4096)
            if not response:
                break
            client_socket.sendall(response)
    except:
        pass
    finally:
        client_socket.close()
        pool_socket.close()

def main():
    """ Jalankan proxy lokal di VPS """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", POOL_PORT))  # Port lokal untuk miner
    server.listen(5)
    
    print(f"✅ Proxy siap di 127.0.0.1:{POOL_PORT}, meneruskan ke {POOL_HOST}:{POOL_PORT} lewat {PROXY_IP}:{PROXY_PORT}")

    while True:
        client_socket, _ = server.accept()
        print("⚡ Miner terhubung!")

        try:
            pool_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            pool_socket.connect((POOL_HOST, POOL_PORT))
        except Exception as e:
            print(f"❌ Gagal konek ke pool: {e}")
            client_socket.close()
            continue

        threading.Thread(target=handle_connection, args=(client_socket, pool_socket)).start()

if __name__ == "__main__":
    main()
