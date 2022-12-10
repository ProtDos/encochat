# Encochat
## beta phase, bugs may appear. The program is finished and ready to use.

## About
High Secured Terminal Chat App

This is a terminal-based chat app that uses advanced encryption and security protocols to ensure that all communications are kept private and secure. To guarantee this, we encrypt every activity you do:
* creating a room
* setting a password
* sending a message
* leaving a room
* joining a room
* creating a private key

## Features

* Millitary encryption used for chat messages
* 1995-bit key exchange for secure communication between users in a group
* Automatic secure deletion of all messages after a person left the group
* Not a single piece in information is send to us: Account information (username/password/creation/activity), messages, groups, contacts and more. All your information is safe
* End-To-End encryption

## Installation and Setup

Make sure you have [Python 3.6](https://python.org/downloads) or later installed on your system.

Clone the repository or [download the zip file](https://github.com/ProtDos/encochat/archive/refs/heads/main.zip) and extract it.

Install the required dependencies using the following command: `pip install -r requirements.txt`

Run the app using the following command: `python chat.py`

```bash
git clone https://github.com/ProtDos/encochat
cd encochat
pip install -r requirements.txt
python3 chat.py  # For Windows users: "py chat.py"
```

## Usage

To start the app, run the command `python3 chat.py` from the app directory.
Follow the on-screen instructions to set up your user account and generate your groups to get in touch with friends.
To start a new chat session, enter number `1` in the main screen and choose a name for the group. This will generate the key to chat with friends.
To send a message, simply type your message and press enter. The message will be encrypted and sent securely to the other users in the group.
To view a list of available commands, check out the `Advanced Usage` tab.

## Advanced Usage
### Creating an account:
```bash
python3 chat.py
[your username] [enter]
2 [enter]
[your password] [enter]
[your password again] [enter]
```

### Creating a room:
```bash
python3 chat.py
1 [enter]
[your password] [enter]
1 [enter]
[room name] [enter]
```

### Joining already used room:
```bash
python3 chat.py
1 [enter]
[your password] [enter]
2 [enter]
1 [enter]
[the number of the group you see under (Your groups)] [enter]
```

### Joining new room:
```bash
python3 chat.py
1 [enter]
[your password] [enter]
2 [enter]
2 [enter]
[the key of the group you got] [enter]
```

### Settings:
Getting into the menu:
```bash
python3 chat.py
1 [enter]
[your password] [enter]
3 [enter]
```
Changing password:

*not possible at the moment*

Changing username:
```bash
2 [enter]
[your username] [enter]
```

Other options

*not possible at the moment*

## Disclaimer
The username you used is shown in our server, but not at what time you connected or whom you wrote. We do not take any responsability for any activity made with this project. We cannot guarantee 100% security, when you find any vulnerabilities, please tell them us as soon as possible.

## TODO:
* ~~In the settings menu: don't use exit function, crashes program directly without text.~~
* ~~In the main menu: change order of numbers (make it before the text)~~
* ~~fix ngrok connections~~
* ~~make error message in chat when server goes down~~ (kinda)
* implement update function
* different colors for every user
* ~~"Press a key to close the chat..."~~
* ~~three tries for password~~
* ~~comment every sequence in the code~~
* split code in different files
* ~~choose at opening between "login" and "register"~~
* change variable names (for better understanding)
* create error logs (for testing purposes) (can be turned on in settings -> store in json format
* make the key smaller
* ~~make function to exit the chat~~
* faster message sending

## Contact

Website: https://protdos.com

Support forum: NaN

Email: rootcode@duck.com

