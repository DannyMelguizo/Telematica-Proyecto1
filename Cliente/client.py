import grpc_server, mom_server
import threading
import os

class Interface:
    def __init__(self, ip):
        self.ip = ip
        self.interface()

    def interface(self):
        while True:
            print("\nSelect a number to navigate through the menu.")
            print("1. List files.")
            print("2. Upload file.")
            print("3. Download file.\n")
            print("0. Exit.\n")

            option = input("Option: ")

            if option == "1":
                print("List of files.")
                files = grpc_server.list_files(self.ip)

                if len(files) == 0:
                    print("There are no files yet.")

                for idx, file in enumerate(files):
                    print(f"{idx+1}. {file}")

                print("\n\n")

                input("\nPress any key to go back to the menu.")

            elif option == "2":
                print("Enter the name of the file to upload.")
                files = list_files()

                if len(files) == 0:
                    print("There are no files to upload.\n")
                    print("Please, add files to the 'files' folder.\n\n")
                    continue

                file = input("File: ")           

                original_file = validate_file(file, files)

                if original_file == False:
                    print("The file does not exist.")
                    continue
        
                grpc_server.send_file(original_file, self.ip)

            elif option == "3":
                print("Enter the name of the file to download.")
                file = input("File: ")

                files = grpc_server.list_files(self.ip)

                if len(files) == 0:
                    print("There are no files to download.\n")
                    continue
                
                original_file = validate_file(file, files)

                if original_file == False:
                    print("The file does not exist in the server.")
                    continue

                thread = threading.Thread(target=mom_server.get_blocks)
                thread.daemon = True
                thread.start()
                grpc_server.get_file(original_file, self.ip)
                input("\nPress any key to go back to the menu.")

            elif option == "0":
                break
            else:
                print("Invalid option.")


def list_files():

    files = []
    path = "files/"

    for file in os.listdir(path):
        print(file)
        files.append(file)
    
    return files

def validate_file(file, list_files):
    file = file.lower()
    for f in list_files:
        if file == f.lower():
            return f
    return False