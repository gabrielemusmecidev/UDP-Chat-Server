import random
import socket
import threading

serverIP = "127.0.0.1"  # Default localhost
porta = 8080  # Default porta 8080

def RiceviData(sock):
    while True:
        try:
            data, indirizzo = sock.recvfrom(1024)
            print(data.decode("utf-8"))
        except Exception as e:
            print(f"Errore nella ricezione dei dati: {e}")
            break

def avviaClient(serverIP, porta):
    host = "127.0.0.1"  # Utilizziamo direttamente l'IP localhost
    client_port = random.randint(6000, 10000)
    print("Ip del Client: " + str(host) + " Porta: " + str(client_port))
    server = (serverIP, porta)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, client_port))
    
    nome = input("Inserisci il tuo nome: ")
    if nome == '':
        nome = 'Anonimo' + str(random.randint(1000, 9999))
        print("Sei " + nome)
    s.sendto(nome.encode("utf-8"), server)
    threading.Thread(target=RiceviData, args=(s,)).start()
    while True:
        data = input()
        if data == 'exit':
            break
        elif data == '':
            continue
        data = '[ ' + nome + ' ]:' + data
        s.sendto(data.encode("utf-8"), server)
    s.sendto(data.encode("utf-8"), server)
    s.close()

if __name__ == "__main__":
    avviaClient(serverIP, porta)
