"""
Author: CodingLive / ProtDos
Title: Encochat
Description: A highly secure end-to-end encrypted chat for everyone that has higher security standards than millitary
Version: Beta 1.0
"""

try:
    import socket  # To connect to the server
    import threading  # Threaded tasks
    from cryptography.fernet import Fernet  # For encrypting messages
    import base64  # For encrypting messages
    from cryptography.hazmat.backends import default_backend  # For encrypting messages
    from cryptography.hazmat.primitives import hashes  # For encrypting messages
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC  # For encrypting messages
    import string  # Generating strong keys
    import random  # Generating strong keys
    import os  # Clearing the terminal window
    import time  # Sleeping function
    import uuid  # Generating unique IDs
    import pyfiglet  # Printing the banner
    from colorama import Fore, Style  # Coloring
    from password_strength import PasswordPolicy  # Checking security of password
except:  # if one of the packages isn't installed
    import os

    os.system("pip install cryptography pyfiglet colorama password-strength")  # Installing missing packages if needed
    os.system("cls")  # clearing window

# TODO: better variable names
# TODO: comment everything
# TODO: different colors for users

try:
    global idd  # globalising variables
    global new_pas

    print(pyfiglet.figlet_format("ENCOCHAT"))  # printing the banner

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating socket for connection to server

    all_threads = []

    # 0.tcp.eu.ngrok.io: 18088
    ipp = socket.gethostbyname("0.tcp.eu.ngrok.io")  # getting ip address of the server
    port = 18088

    try:
        client.connect((ipp, port))  # connecting to the server
    except:  # not working with ngrok, still leaving it
        os.system("cls")
        exit("[-] Server is offline.")


    def username_check_create():
        # globalising variables
        global idd
        global nickname
        if not os.path.isfile("username.txt"):  # checking if username already has been set
            nickname = input(Fore.BLUE + "Enter your username: " + Style.RESET_ALL)  # if not, create a new username
            if "|||" in nickname:  # for
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


    username_check_create()  # calling function


    def update():
        # TODO: coming soon...
        pass


    def password_check(_):  # unnecessary
        return {
            'password_ok': True
        }


    def strength_test(p):
        policy = PasswordPolicy.from_names(
            length=12,  # min length: 12
            uppercase=2,  # need min. 2 uppercase letters
            numbers=2,  # need min. 2 digits
            special=2,  # need min. 2 special characters
            nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
        )
        out = policy.test(p)
        return [True if out == [] else False]  # returning if password is good or not


    def gen(length):
        al = string.ascii_uppercase + string.ascii_lowercase + string.digits + "^!§$%&/()=?*+#'-_.:;{[]}"  # creating a list of nearly every char
        bb = []  # init list
        for i in range(length):  # creating a random password based on var length
            bb.append(random.choice(al))
        return "".join(bb)  # TODO: smaller key


    class Encrypt:
        def __init__(self, message_, key):
            self.message = message_
            self.key = key

        def encrypt(self):  # TODO: faster
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
                message__ = client.recv(1024).decode('ascii')  # getting messages
                if message__ == 'NICK':
                    client.send(
                        nickname.encode('ascii'))  # telling the server our nickname, which is seen by other users
                else:
                    out = Decrypt(message__, key, verbose=False).decrypt()  # decrypting incoming message
                    if out is not None:  # checking if message is decrypted correctly
                        print(out)
            except Exception as e:
                if str(e) == "[WinError 10053] An established connection was aborted by the software in your host machine":
                    exit("Server is closed...")
                    break
                print(e)
                print("[-] An error occurred!")
                client.close()
                break
        exit("Server is closed...")


    def write(key):
        while True:
            try:
                lll = input('> ')  # getting user input
                if lll == "exit()":  # if message is exit(), close the connection
                    os.system("cls")
                    print("Cya...")
                    for item in all_threads:
                        item.join()
                    client.close()  # closing connection
                    exit()

                elif "|||" in lll:
                    print("[-] You are not allowed to have a '|||' in your message.")
                else:
                    message_ = '{}: {}'.format(nickname, lll)
                    try:
                        client.send(Encrypt(message_, key).encrypt())  # sending message to the server
                    except ConnectionAbortedError:
                        exit("Server is down. Please try again later.")
                        break
                    except KeyboardInterrupt:
                        exit("Ctrl+C detected.")
            except KeyboardInterrupt:
                exit("Ctrl+C detected.")


    def change_username():
        u = input("Enter username: ")
        f = open("username.txt", "w")
        f.write(u)
        f.close()


    def auth():
        global new_pas
        abfrage_auth = int(input("(1) Login or (2) Register: "))  # letting user to choose
        if abfrage_auth == 1:  # when he wants to login
            if os.path.isfile("auth.txt"):  # checking if auth.txt file exists
                for i in range(3):  # three tries
                    password = input("Please enter your password: ")  # user input for password
                    with open("auth.txt") as file:  # opening file
                        data = file.read()  # getting content
                    dec_pass = Decrypt(message_=data, key=password).decrypt()  # checking if password is the same
                    if dec_pass == password:
                        print("[+] Successfully verified.")
                        new_pas = dec_pass
                        break
                    else:
                        print(f"[-] Wrong password. {i} tries left.")
                    if i == 3:
                        exit("Too many failed attempts.")

            else:
                print("[-] No account found, please register first.")  # register function
                print(
                    "Password must contain: at least 12 chars, 2 uppercase, 2 numbers, 2 special characters, 2 non-letters.")  # for highest security
                while True:
                    p1 = input("Please create a password: ")
                    if strength_test(p1):
                        break
                    else:
                        print("[-] Password is not strong enough. Please try again.")
                p2 = input("Please retype password: ")
                if p1 == p2:
                    pass
                else:
                    print("The passwords do not match.")
                    input("Press enter to continue...")
                with open("auth.txt", "w") as file:
                    file.write(
                        Encrypt(message_=p1, key=p1).encrypt().decode())  # encrypting password for login function
                print("[+] Your account has been created.")
                new_pas = p1
        else:  # same thing again
            print("[-] No account found, please register first.")
            print(
                "Password must contain: at least 12 chars, 2 uppercase, 2 numbers, 2 special characters, 2 non-letters.")
            while True:
                p1 = input("Please create a password: ")
                if strength_test(p1):
                    break
                else:
                    print("[-] Password is not strong enough. Please try again.")
            p2 = input("Please retype password: ")
            if p1 == p2:
                pass
            else:
                exit("They are not the same...")
            with open("auth.txt", "w") as file:
                file.write(Encrypt(message_=p1, key=p1).encrypt().decode())
            print("[+] Your account has been created.")
            new_pas = p1


    def main():
        super_dubba_key = ""
        try:
            super_dubba_key = f"{idd}|||{new_pas}"  # creating key to save group key
        except:  # if user changed the code to remove auth function
            exit("Please authenticate...")

        """
        When for example a hacker tries to get the group keys and removes the auth function and/or changes 
        'super_dubba_key', the groups won't be encrypted, because the key isn't the same.
        So please never share your password with anyone, because else they have a way into all of your chats.
        """

        os.system("title ENCOCHAT")
        os.system("cls")
        print(pyfiglet.figlet_format("ENCOCHAT"))
        print(Fore.BLUE + "Your groups (please wait!):" + Style.RESET_ALL)  # loading groups
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
        my_bitch_rooms = [""]  # list of rooms
        try:
            for i in range(1, len(data)):
                try:
                    if data[i] == "":
                        pass
                    else:
                        current_line = Decrypt(message_=data[i], key=super_dubba_key,
                                               verbose=False).decrypt()  # decrypting every group name/key
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
        i = int(input("(1) Create room, (2) Join a room, (3) Settings, (4) Exit: "))
        print("")

        if i == 1:
            name = input("Enter a group name (max. 20 char): ")
            if name == "":
                print(Fore.RED + "[-] Please enter a valid group name." + Style.RESET_ALL)
                input("Press enter to continue...")
                main()
            key = gen(1979)
            key = name + "|" + key

            with open("groups.csv", "a") as file:
                file.write(f"{Encrypt(message_=key, key=super_dubba_key).encrypt().decode()}\n")
            print(Fore.GREEN + "[+] Room created." + Style.RESET_ALL)

            print(Fore.GREEN + "The key is: \n" + key + Style.RESET_ALL)
            print("\n\nUse it for others to join the chat.")
            print("Chat started. Press Ctrl+C to exit.")

            os.system(f"title {name}")

            receive_thread = threading.Thread(target=receive, args=(key,))
            receive_thread.start()

            all_threads.append(receive_thread)

            write_thread = threading.Thread(target=write, args=(key,))
            write_thread.start()

            all_threads.append(write_thread)
        elif i == 2:
            mf = int(input("(1) Join an old group or (2) new group: "))
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
                    input("Press enter to continue...")
                    main()

                if len(str(key)) < 1000:
                    exit("Invalid key.")

                os.system(f"title {name}")
                os.system("cls")
                print("Chat started. Press Ctrl+C to exit.")

                receive_thread = threading.Thread(target=receive, args=(key,))
                receive_thread.start()

                all_threads.append(receive_thread)

                write_thread = threading.Thread(target=write, args=(key,))
                write_thread.start()

                all_threads.append(write_thread)
            elif mf == 2:
                key = input("Enter the key: ")

                if len(key) < 1000:
                    print("Invalid key.")
                    input("Press enter to exit...")

                try:
                    os.system(f"title {key.split('|')[0]}")
                except:
                    print("Invalid key.")
                    input("Press enter to exit...")

                with open("groups.csv", "a") as file:
                    file.write(f"{Encrypt(message_=key, key=super_dubba_key).encrypt().decode()}\n")

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
            print("5) Logging options")
            print("6) Go back.")
            a = int(input("> "))
            if a == 1:
                print(
                    Fore.RED + "[-] Changing your password is not possible. Please contact support for more information." + Style.RESET_ALL)
            elif a == 2:
                change_username()
                input("Press enter to continue...")
                main()
            elif a == 3:
                print(Fore.RED + "[-] Not ready yet." + Style.RESET_ALL)
                input("Press enter to continue...")
                main()
            elif a == 4:
                print(Fore.RED + "[-] Not ready yet." + Style.RESET_ALL)
                input("Press enter to continue...")
                main()
            elif a == 5:
                print(Fore.RED + "[-] Not ready yet." + Style.RESET_ALL)
                input("Press enter to continue...")
                main()
            elif a == 6:
                main()
            else:
                print(Fore.RED + "[-] Wrong choice." + Style.RESET_ALL)
                input("Press enter to continue...")
                main()
        elif i == 4:
            os.system("cls")
            exit("Cya...")
        else:
            print(Fore.RED + "[-] Wrong choice." + Style.RESET_ALL)
            input("Press enter to continue...")
            main()


    if __name__ == "__main__":
        auth()  # without this function, you can't really do anything
        main()  # start the main part
except KeyboardInterrupt:
    exit("Cya.")
