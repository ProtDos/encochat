import socket
import threading
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import string
import random
import os
import time
import uuid
import shutil
import pyfiglet
from colorama import Fore, Style
import getpass

try:
    global idd
    global new_pas

    os.system("cls")


    def print_centre(s):
        print(s.center(shutil.get_terminal_size().columns))


    print(pyfiglet.figlet_format("ENCOCHAT"))

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    all_threads = []

    try:
        client.connect(('4.tcp.ngrok.io', 11596))
    except:
        os.system("cls")
        exit("[-] Server is offline.")

    if not os.path.isfile("username.txt"):
        nickname = input(Fore.BLUE + "Create your username: " + Style.RESET_ALL)
        if "|||" in nickname:
            exit("Sorry, for technical reasons you can't have a '|||' in your nickname.")
        else:
            open("username.txt", "w").write(nickname)
            print(Fore.GREEN + "[+] Nickname is set." + Style.RESET_ALL)
    else:
        nickname = open("username.txt", "r").read()
        if "|||" in nickname:
            exit("Sorry, you can't have a '|||' in your nickname. Please change it.")
    client.send(nickname.encode())
    idd = nickname


    def password_check(_):
        return {
            'password_ok': True
        }


    def gen(length):
        al = string.ascii_uppercase + string.ascii_lowercase + string.digits + "^!§$%&/()=?*+#'-_.:;{[]}"
        bb = []
        for i in range(length):
            bb.append(random.choice(al))
        return "".join(bb)


    class Encrypt:
        def __init__(self, message_, key):
            self.message = message_
            self.key = key

        def encrypt(self):
            password_provided = self.key
            password = password_provided.encode()
            salt = b'salt_'
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=10000000,
                backend=default_backend()
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
            msg = self.message.encode()
            f = Fernet(key)
            msg = f.encrypt(msg)
            return msg


    class Decrypt:
        def __init__(self, message_, key, verbose=True):
            self.message = message_
            self.key = key
            self.verbose = verbose

        def decrypt(self):
            try:
                self.key = self.key.encode()
                ss = time.time()
                salt = b'salt_'
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=10000000,
                    backend=default_backend()
                )
                key = base64.urlsafe_b64encode(kdf.derive(self.key))
                self.message = self.message.encode()
                f = Fernet(key)
                decoded = str(f.decrypt(self.message).decode())
                return decoded
            except:
                pass


    def receive(key):
        while True:
            try:
                message__ = client.recv(1024).decode('ascii')
                if message__ == 'NICK':
                    client.send(nickname.encode('ascii'))
                else:
                    out = Decrypt(message__, key, verbose=False).decrypt()
                    if out is not None:
                        print(out)
            except:
                print("[-] An error occurred!")
                client.close()
                break


    def write(key):
        while True:
            try:
                lll = input('> ')
                if lll == "exit()":
                    os.system("cls")
                    print("Cya...")
                    for item in all_threads:
                        item.join()
                    exit()
                elif "|||" in lll:
                    print("[-] You are not allowed to have a '|||' in your message.")
                else:
                    message_ = '{}: {}'.format(nickname, lll)

                    client.send(Encrypt(message_, key).encrypt())
            except KeyboardInterrupt:
                exit("Ctrl+C detected.")


    def change_username():
        u = input("Enter username: ")
        open("username.txt", "w").write(u)


    def auth():
        global new_pas
        if os.path.isfile("auth.txt"):
            password = input("Please enter your password: ")
            with open("auth.txt") as file:
                data = file.read()
            dec_pass = Decrypt(message_=data, key=password).decrypt()
            if dec_pass == password:
                print("[+] Successfully verified.")
            else:
                exit("Wrong password")
            new_pas = dec_pass
        else:
            p1 = input("Please create a password: ")
            p2 = input("Please retype password: ")
            if p1 == p2:
                pass
            else:
                exit("They are not the same...")
            with open("auth.txt", "w") as file:
                file.write(Encrypt(message_=p1, key=p1).encrypt().decode())
            print("[+] Your account has been created.")
            new_pas = p1
    auth()


    def main():
        super_dubba_key = f"{idd}|||{new_pas}"
        os.system("title ENCOCHAT")
        os.system("cls")
        print(pyfiglet.figlet_format("ENCOCHAT"))
        print(Fore.BLUE + "Your groups (please wait!):" + Style.RESET_ALL)
        try:
            with open("groups.csv") as file:
                data = file.read().split("\n")
        except:
            if not os.path.isfile("groups.csv"):
                a = open("groups.csv", "w")
                a.write("key\n")
                a.close()
            data = []
        c = 0
        my_bitch_rooms = [""]
        try:
            for i in range(1, len(data)):
                try:
                    if data[i] == "":
                        pass
                    else:
                        current_line = Decrypt(message_=data[i], key=super_dubba_key, verbose=False).decrypt()
                        print(f"{i}) {current_line.split('|')[0]} | {current_line.split('|')[1][:15]}")
                        my_bitch_rooms.append(current_line)
                        c += 1
                except:
                    c -= 1
                    pass
        except:
            pass
        if c <= 0:
            print(Fore.YELLOW + "[-] No rooms to show." + Style.RESET_ALL)

        print("\nChoose your action:")
        i = int(input("Create room (1), Join a room (2), Settings (3), Exit (4): "))
        print("")

        if i == 1:
            name = input("Enter a group name (max. 20 char): ")
            if name == "":
                print(Fore.RED + "[-] Please enter a valid group name." + Style.RESET_ALL)
                time.sleep(1)
                main()
            key = gen(1979)
            key = name + "|" + key

            with open("groups.csv", "a") as file:
                file.write(f"{Encrypt(message_=key, key=super_dubba_key).encrypt().decode()}")
            print(Fore.GREEN + "[+] Room created." + Style.RESET_ALL)

            print(Fore.GREEN + "The key is: \n" + key + Style.RESET_ALL)
            print("\n\nUse it for others to join the chat.")
            print("Chat started. Type 'exit()' to exit.")

            os.system(f"title {name}")

            receive_thread = threading.Thread(target=receive, args=(key, ))
            receive_thread.start()

            all_threads.append(receive_thread)

            write_thread = threading.Thread(target=write, args=(key, ))
            write_thread.start()

            all_threads.append(write_thread)
        elif i == 2:
            mf = int(input("Join an old group (1) or new group (2): "))
            if mf == 1:
                key = ""  # ignore
                name = ""  # ignore
                print("")
                num = int(input("Enter number of group: "))
                try:
                    key = my_bitch_rooms[num].split("|")[1]
                    name = my_bitch_rooms[num].split("|")[0]
                except:
                    print(Fore.RED + "[-] Invalid number." + Style.RESET_ALL)
                    main()

                if len(str(key)) < 1000:
                    exit("Invalid key.")

                os.system(f"title {name}")
                os.system("cls")
                print("Chat started. Type 'exit()' to exit.")

                receive_thread = threading.Thread(target=receive, args=(key,))
                receive_thread.start()

                all_threads.append(receive_thread)

                write_thread = threading.Thread(target=write, args=(key,))
                write_thread.start()

                all_threads.append(write_thread)
            elif mf == 2:
                key = input("Enter the key: ")

                if len(key) < 1980:
                    exit("Invalid key.")

                try:
                    os.system(f"title {key.split('|')[0]}")
                except:
                    exit("Invalid key.")

                os.system("cls")

                receive_thread = threading.Thread(target=receive, args=(key,))
                receive_thread.start()

                write_thread = threading.Thread(target=write, args=(key,))
                write_thread.start()
        elif i == 3:
            print("1) Change password.")
            print("2) Change username.")
            print("3) Delete everything.")
            print("4) Delete a group.")
            print("5) Go back.")
            a = int(input("> "))
            if a == 1:
                print(Fore.RED + "[-] Changing your password is not possible. Please contact support for more information." + Style.RESET_ALL)
            elif a == 2:
                change_username()
                main()
            elif a == 3:
                print(Fore.RED + "[-] Not ready yet." + Style.RESET_ALL)
                main()
            elif a == 4:
                pass
            elif a == 5:
                main()
            else:
                print(Fore.RED + "[-] Wrong choice." + Style.RESET_ALL)
                main()
        elif i == 4:
            os.system("cls")
            exit("Cya...")
        else:
            print(Fore.RED + "[-] Wrong choice." + Style.RESET_ALL)
            main()


    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    exit("Cya.")
