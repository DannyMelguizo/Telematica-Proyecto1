import config_file
import re
import socket

def main():
    config_file.create_config_file()
    print("Welcome to the DataNode.")
    ip = input("Enter the IP of the Server:")

    while validate_ip(ip) == False:
        if ip == "localhost":
            break
        ip = input("Enter a valid IP: ")
    
    config_file.set_ip(ip)

    connect_to_server()
    send_file("file.txt", 1)




def connect_to_server(data = None):
    port = config_file.get_port()
    ip = config_file.get_ip()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip, port))

    if data:
        server.send(data.encode())
        response = server.recv(1024).decode()
        print(response)


def send_file(file_name, block):

    data = {
        "file_name": file_name,
        "block": block
    }

    connect_to_server(data)



    

def validate_ip(ip):
    pattern = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

    if ip == "0.0.0.0":
        return False

    #Verify if the ip given is valid
    if re.match(pattern, ip):
        return True
    else:
        return False


if __name__ == '__main__':

    main()