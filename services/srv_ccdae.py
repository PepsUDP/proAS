import socket, json
from db_uci import dbuci
from comunicacion import sendT, listenB, registerS
srv = 'ccdae'

#Agregar entidad
def addE(opcion, rgtr):
    crsr = dbuci.cursor()
    fetched = None
    if opcion == 1:
        crsr.execute("INSERT INTO pasillo (estado) VALUES (%s)", (rgtr[0],))
        dbuci.commit()
        response = {"respuesta":"El pasillo ha sido ingresado exitosamente."}
        sendT(sckt, srv, json.dumps(response))
    elif opcion == 2:
        print(rgtr)
        crsr.execute("INSERT INTO sala (id_sala, cantCamas, camasDisp, estado) VALUES (%s, %s, %s, %s)", (rgtr[0], rgtr[1], rgtr[1], rgtr[2]))
        dbuci.commit()
        response = {"respuesta":"La pieza ha sido ingresada exitosamente."}
        sendT(sckt, srv, json.dumps(response))
    elif opcion == 3:
        print(rgtr)
        crsr.execute("INSERT INTO personalLimpieza (RUT, nombre, fechaNac, disponible) VALUES (%s, %s, %s, %s)", (rgtr[0], rgtr[1], rgtr[2], 1))
        dbuci.commit()
        response = {"respuesta":"El empleado de limpieza ha sido ingresado exitosamente."}
        sendT(sckt, srv, json.dumps(response))

if __name__ == "__main__":
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('localhost', 5000)
        print('Servicio: Conectándose a {} puerto {}'.format(*server_address))
        sckt.connect(server_address)
    except:
        print('No es posible la conexión al bus')
        quit()

    registerS(sckt, srv)

    while True:
        nS, mT = listenB(sckt)
        print(nS, mT)
        print(mT)
        if nS == srv:
            l = []
            mTloads = json.loads(mT)
            print(mTloads["opcion"])
            if mTloads["opcion"] == 1:
                l.append(mTloads["estado"])
                addE(opcion = mTloads["opcion"], rgtr = l)
            elif mTloads["opcion"] == 2:
                l.append(mTLoads["id_sala"])
                l.append(mTloads["cantCamas"])
                l.append(mTloads["estado"])
                addE(opcion = mTloads["opcion"], rgtr = l)
            elif mTloads["opcion"] == 3:
                l.append(mTLoads["RUT"])
                l.append(mTloads["nombre"])
                l.append(mTloads["fechaNac"])
                l.append(mTloads["disponible"])
        else:
            response = {"respuesta":"servicio incorrecto"}
            sendT(sckt, srv, json.dumps(response))

    print('Se cierra socket')
    sckt.close()