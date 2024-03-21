import grpc_server, mom_server
import threading

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

                for idx, file in enumerate(files):
                    print(f"{idx+1}. {file}")

                input("\nPress any key to go back to the menu.")

            elif option == "2":
                print("Enter the name of the file to upload.")
                file = input("File: ")
                grpc_server.send_file(file, self.ip)

            elif option == "3":
                print("Enter the name of the file to download.")
                file = input("File: ")
                threading.Thread(target=mom_server.get_blocks).start()
                grpc_server.get_file(file, self.ip)



            elif option == "0":
                break
            else:
                print("Invalid option.")
