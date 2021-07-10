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
    menu = f"""
    Registro de usuario
    Elija un rol:

    1) Usuario administrador
    2) Usuario general
    """
    rol = input(menu)
    if rol in ["1","2"]:
        username = menuRgtrUN()
        password = menuRgtrPW()
    else:
        return menuRgtrROL()
    menuConfirmar = """
    Registro de usuario
    Usuario: {username}
    Rol: {"Administrador" if rol == "1" else "General"}
    ¿Son estos datos correctos? [y/n]
    """
    yn = input(menuConfirmar)
    if yn == 'y':
        arg = {"username": username, "password": password, "rol": rol}
        sendT(sckt, json.dumps(arg), rgtr)
        nS, msgT =listenB(sckt)
        msg = json.loads(msgT[2:])
        if nS == rgtr:
            if msg["respuesta"]:
                print(msg["respuesta"])
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