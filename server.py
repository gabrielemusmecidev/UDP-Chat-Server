import queue
import socket
import threading

host = "127.0.0.1"  # Default localhost
porta = 8080  # Default porta 8080

def RiceviData(sock, recvPacket):
    while True:
        data, indirizzo = sock.recvfrom(1024)
        recvPacket.put((data, indirizzo))

def avviaServer():
    print("Server hostato su %s e porta %d" % (host, porta))
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, porta))
    clients = set()
    recvPacket = queue.Queue()
    print("In attesa di connessioni...")
    threading.Thread(target=RiceviData, args=(s, recvPacket)).start()

    while True:
        data, indirizzo = recvPacket.get()
        if indirizzo not in clients:
            clients.add(indirizzo)
            print(f"Nuovo client connesso: {indirizzo}")

        # Decodifica del messaggio spostata qui
        message = data.decode('utf-8')
        
        if message.endswith("exit"):
            clients.remove(indirizzo)
            print(f"Client disconnesso: {indirizzo}")
            continue

        print(str(indirizzo) + ": " + message)
        for client in clients:
            if client != indirizzo:
                # Rimosso data.encode('utf-8') poiché 'data' è già in bytes
                s.sendto(data, client)

    s.close()

if __name__ == "__main__":
    avviaServer()
