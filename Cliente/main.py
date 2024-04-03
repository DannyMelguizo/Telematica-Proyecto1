import config_file, client
import re
def main():
    config_file.create_config_file()
    ip = input("Enter the IP of the Server:")

    while validate_ip(ip) == False:
        if ip == "localhost":
            break
        ip = input("Enter a valid IP: ")

    client.Interface(ip)
    

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