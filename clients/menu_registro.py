import socket, sys, json
from os import system, name
from comunicacion import clearS, sendT, listenB
rgtr = "sgnup"

sesion = {"id": None, "username": None, "rol": None}
sckt = None

def menuRgtrPW():
    clearS()
    menu = """
    Registro de usuario
    Ingrese una contraseña: """
    password = input(menu)
    return password

def menuRgtrUN():
    clearS()
    menu = """
    Registro de usuario
    Ingrese un nombre de usuario: """
    username = input(menu)
    return username

def menuRgtrROL():
    rol = None
    username = None
    password = None
    clearS()
    menu = """
    Registro de usuario
    Elija un rol:

    1) Usuario administrador
    2) Usuario general
    """
    clearS()
    rol = input(menu)
    if rol in ["1","2"]:
        username = menuRgtrUN()
        clearS()
        password = menuRgtrPW()
        clearS()
    else:
        return menuRgtrROL()
    menuConfirmar = f"""
    Registro de usuario
    Usuario: {username}
    Contraseña: {password}
    Rol: {"Administrador" if rol == "1" else "General"}
    ¿Son estos datos correctos? [y/n]
    """
    clearS()
    yn = input(menuConfirmar)
    if yn == 'y':
        arg = {"username": username, "password": password, "rol": rol}
        print(arg)
        sendT(sckt, rgtr, json.dumps(arg))
        nS, msgT = listenB(sckt)
        print(msgT)
        msg = json.loads(json.dumps(msgT[2:]))
        print(msg)
        if nS == rgtr:
            if msg[1]:
                print(msg[1])
    else:
        menuRgtrROL()

if __name__ == "__main__":
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 5000)
        print('Cliente: Conectándose a {} puerto {}'.format(*server_address))
        sckt.connect(server_address)
    except:
        print('No es posible la conexión al bus')
        quit()
    
    menuRgtrROL()