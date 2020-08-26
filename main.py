from HttpServer import HttpServer
import socket

if __name__ == "__main__":
    IP_ADDRESS = socket.gethostbyname(socket.gethostname())
    LOCALHOST = "127.0.0.1"

    print("Do you want to run this on localhost or your IP?")
    print("[1] My IP -", IP_ADDRESS + ":8000")
    print("[2] localhost -", LOCALHOST + ":8000")

    choice = input()
    if choice == "1":
        BIND_IP = IP_ADDRESS
        
    elif choice == "2":
        BIND_IP = LOCALHOST
    else:
        print("That is not a valid option!")

    server = HttpServer(bind_ip=BIND_IP)
    server.start()