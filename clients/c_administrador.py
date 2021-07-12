import socket, json
from os import system, name
from comunicacion import clearS, sendT, listenB
rgtr = "ccdsu"  # Registro
lgin = "ccdli"  # Ingreso
aden = "ccdae"  # Agregar entidad
gtdb = "ccddb"  # Consultar datos

sesion = {"username":None,"password":None,"rol":None}
sckt = None

def menuSULI():
    clearS()
    menu = """
    ***************************************
    * Usuario administrador               *
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
    rol = 1 # Usuario administrador
    clearS()

    menuUN = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Registro de usuario                 *
    * Ingresar nombre de usuario          *
    ***************************************

    Usuario: """    
    clearS()
    username = input(menuUN)

    menuPW = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Registro de usuario                 *
    * Ingresar contraseña                 *
    ***************************************
    
    Contraseña: """
    clearS()
    password = input(menuPW)

    menuYN = f"""
    ***************************************
    * Usuario administrador               *
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
        arg = {"username": username, "password": password, "rol": "1"}
        print(arg)
        sendT(sckt, rgtr, json.dumps(arg))
        nS, msgT = listenB(sckt)
        print(msgT)
        msg = json.loads(msgT[12:])
        print(nS)
        print(msgT)
        if nS == rgtr:
            if msg["respuesta"]:
                print(msg["respuesta"])
    else:
        menuSU()

def menuLI():
    username = None
    password = None
    #rol = 1 # Usuario administrador

    menuUN = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Inicio de sesión                    *
    * Ingresar nombre de usuario          *
    ***************************************

    Usuario: """   
    clearS()
    username = input(menuUN)

    menuPW = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Inicio de sesión                    *
    * Ingresar contraseña                 *
    ***************************************
    
    Contraseña: """
    clearS()
    password = input(menuPW)

    arg = {"username": username, "password": password, "rol": 1}
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
            if sesion["rol"] == 1:
                # Menu cliente
                #print("menuCliente()")
                menuCRUD()
            else:
                menuLI()

def menuCRUD():
    clearS()
    menuCRUD2 = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Menu                                *
    * Elija una opción                    *
    *-------------------------------------*
    * 1) Agregar entidad                  *
    * 2) Eliminar entidad                 *
    * 3) Asignar equipo a paciente        *
    * 4) Asignar medico a paciente        *
    * 5) Consultar datos                  *
    *                                     *
    * 6) Cerrar sesión                    *
    ***************************************
    
    Opción: """
    opcion = int(input(menuCRUD2))
    if opcion == 6:
        menuSULI()
    elif opcion == 1:
        menuAE()
    elif opcion == 2:
        print("2")
    elif opcion == 3:
        print("3")
    elif opcion == 4:
        print("4")
    elif opcion == 5:
        menuGD()

def menuGD():
    menuGD2 = """
    ***************************************
    * Usuario administrador               *
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
    *                                     *
    * 7) Cerrar sesión                    *
    ***************************************
    
    Opción: """
    opcion = int(input(menuGD2))
    if opcion == 7:
        menuSULI()
    else:
        arg = {"opcion": opcion}
        sendT(sckt, gtdb, json.dumps(arg))
        nS, msgT = listenB(sckt)
        msg = msgT[12:]
        if nS == gtdb:
            if msg:
                print(msg)

                enter = input("Presione enter para continuar. ")
                clearS()
                menuGD()

def menuAE():
    clearS()
    menuAE2 = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Agregar entidad                     *
    * Elija una opción                    *
    *-------------------------------------*
    * 1) Pasillos                         *
    * 2) Piezas                           *
    * 3) Personal Limpieza                *
    * 4) Pacientes                        *
    * 5) Personal Médico                  *
    * 6) Equipo Médico                    *
    *                                     *
    * 7) Cerrar sesión                    *
    ***************************************
    
    Opción: """
    opcion = int(input(menuAE2))
    if opcion == 7:
        menuSULI()
    else:
        list = []
        inpt = None
        if opcion == 1:
            pa=["Estado (Si = 1, No = 0)"]
            for i in pa:
                print("Ingrese ", i, ": ")
                inpt = input()
                list.append(inpt)
            arg = {"opcion": opcion, "estado": list[0]}
        elif opcion == 2:
            sa=["ID de cama", "Cantidad de camas"]
            for i in sa:
                print("Ingrese ", i, ": ")
                inpt = input()
                list.append(inpt)
            arg = {"opcion": opcion, "id_sala": list[0], "cantCamas": list[1], "estado": "Limpio"}
        elif opcion == 3:
            pl=["RUT", "Nombre", "Fecha de nacimiento"]
            for i in pl:
                print("Ingrese ", i, ": ")
                inpt = input()
                list.append(inpt)
            arg = {"opcion": opcion, "RUT": list[0], "nombre": list[1], "fechaNac": list[2], "disponible": 1}
        elif opcion == 4:
            pc=["RUT", "Nombre", "Fecha de nacimiento (YYYY-MM-DD)", "Edad", "Enfermedad", "Sintomas", "Dieta", "Alergias", "Medicamentos", "Tratamiento"]
            for i in pc:
                print("Ingrese ", i, ": ")
                inpt = input()
                list.append(inpt)
            arg = {"opcion": opcion, "RUT": list[0], "nombre": list[1], "fechanac": list[2], "edad": list[3], "enfermedad": list[4], "sintomas": list[5], "dieta": list[6], "alergias": list[7], "medicamentos": list[8], "tratamiento": list[9]}
        elif opcion == 5:
            pm=["RUT", "Nombre", "Fecha de nacimiento", "Especialidad"]
            for i in pm:
                print("Ingrese ", i, ": ")
                inpt = input()
                list.append(inpt)
            arg = {"opcion": opcion, "RUT": list[0], "nombre": list[1], "fechanac": list[2], "especialidad": list[3], "disponible": 1}
        elif opcion == 6:
            em=["Tipo de equipo medico", "Fecha de inicio de uso (YYYY-MM-DD)", "Tiempo de uso (horas)"]
            for i in em:
                print("Ingrese ", i, ": ")
                inpt = input()
                list.append(inpt)
            arg = {"opcion": opcion, "u_paciente_RUT": 0, "tipo": list[0], "fechaInicio": list[1], "tiempoUso": list[2], "estado": "Disponible"}
        sendT(sckt, aden, json.dumps(arg))
        nS, msgT = listenB(sckt)
        msg = msgT[12:]
        if nS == aden:
            if msg:
                print(msg)
                enter = input("Presione enter para continuar. ")
                clearS()
                menuAE()

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