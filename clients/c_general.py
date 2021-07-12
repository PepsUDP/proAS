import socket, json
from os import system, name
from comunicacion import clearS, sendT, listenB
from db_uci import dbuci
rgtr = "sgnup"  # Registro
lgin = "ccdli"  # Ingreso
gtdb = "ccddb"  # Consultar datos

sesion = {"username":None,"password":None,"rol":None}
sckt = None

def menuSULI():
    clearS()
    menu = """
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Elija una opción:                   *
    * 1) Sign up (Registrar un usuario)   *
    * 2) Log in (Ingresar con usuario)    *
    ***************************************

    Opción: """
    option = input(menu)
    if option == "1":
        menuSU()
    elif option =="2":
        menuLI()
    else:
        print("Opción ingresada no válida.")
        menuSULI()

def menuSU():
    username = None
    password = None
    rol = 2 # Usuario general
    clearS()

    menuUN = """
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Registro de usuario                 *
    * Ingresar nombre de usuario          *
    ***************************************

    Usuario: """    
    clearS()
    username = input(menuUN)

    menuPW = """
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Registro de usuario                 *
    * Ingresar contraseña                 *
    ***************************************
    
    Contraseña: """
    clearS()
    password = input(menuPW)

    menuYN = f"""
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Registro de usuario                 *
    * Confirme sus datos [y/n]            *
    ***************************************
    
    Usuario: {username}
    Contraseña: {password}
    Rol: {"Administrador" if rol == "1" else "General"}
    
    Opción: """
    clearS()
    yn = input(menuYN)
    if yn == 'y':
        arg = {"username": username, "password": password, "rol": "2"}
        print(arg)
        sendT(sckt, rgtr, json.dumps(arg))
        nS, msgT = listenB(sckt)
        print(msgT)
        msg = json.loads(msgT[12:])
        print(nS)
        print(msgT)
        print("test", msg)
        if nS == rgtr:
            if msg["respuesta"]:
                print(msg["respuesta"])
    else:
        menuSU()

def menuLI():
    username = None
    password = None
    #rol = 2 # Usuario general

    menuUN = """
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Inicio de sesión                    *
    * Ingresar nombre de usuario          *
    ***************************************

    Usuario: """   
    clearS()
    username = input(menuUN)

    menuPW = """
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Inicio de sesión                    *
    * Ingresar contraseña                 *
    ***************************************
    
    Contraseña: """
    clearS()
    password = input(menuPW)

    arg = {"username": username, "password": password, "rol": 2}
    #arg = {"username": username, "password": password, "rol": rol}
    print(arg)
    sendT(sckt, lgin, json.dumps(arg))
    nS, msgT=listenB(sckt)
    print(msgT)
    msg = json.loads(msgT[12:])
    print(msg)
    if nS == lgin:
        if msg["respuesta"] == "No es posible entrar con el usuario ingresado.":
            input("No se ha podido iniciar sesión.")
            menuLI() 
        else:
            global sesion
            sesion=msg["respuesta"]
            print(sesion)
            if sesion["rol"] == 2:
                # Menu cliente
                #print("menuCliente()")
                menuGD()
            else:
                menuLI()

def menuGD():
    menuGD = """
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Consultar datos                     *
    * Elija una opción                    *
    *-------------------------------------*
    * 1) Pasillos                         *
    * 2) Piezas                           *
    * 3) Camas                            *
    * 4) Pacientes                        *
    * 5) Personal Médico                  *
    * 6) Respiradores                     *
    ***************************************
    
    Opción: """
    opcion = int(input(menuGD))
    fetched = None
    crsr = dbuci.cursor()
    if opcion == 1:
        crsr.execute("SELECT * FROM pasillo;")   
        fetched = crsr.fetchall()
    elif opcion == 2:
        crsr.execute("SELECT * FROM sala;")
        fetched = crsr.fetchall()     
    elif opcion == 3:
        crsr.execute("SELECT * FROM equipoMedico WHERE tipo=cama;")   
        fetched = crsr.fetchall() 
    elif opcion == 4:
        crsr.execute("SELECT * FROM paciente;") 
        fetched = crsr.fetchall()
    elif opcion == 5:
        crsr.execute("SELECT * FROM personalMedico;")
        fetched = crsr.fetchall()
    elif opcion == 6:    
        crsr.execute("SELECT * FROM equipoMedico WHERE tipo=respirador;")
        fetched = crsr.fetchall()
    print(fetched)

if __name__ == "__main__":
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('localhost', 5000)
        print('Cliente: Conectandose a {} puerto {}'.format(*server_address))
        sckt.connect(server_address)
    except: 
        print('No es posible la conexión al bus')
        quit()

    menuSULI()