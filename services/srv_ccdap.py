import socket, json
from db_uci import dbuci
from comunicacion import sendT, listenB, registerS
srv = 'ccdap'

#Asignar personal
def asiP(opcion, rgtr):
    crsr = dbuci.cursor()
    fetched = None
    print(rgtr)
    if opcion == 1:
        crsr.execute("UPDATE equipoMedico SET u_paciente_RUT = %s, fechaInicio = %s, tiempoUso = %s, estado = %s WHERE id_equipoMedico = %s", (rgtr[1],rgtr[2],rgtr[3],rgtr[4],rgtr[0]))
        dbuci.commit()
        response = {"respuesta":"La cama ha sido asignada exitosamente."}
        sendT(sckt, srv, json.dumps(response))
    elif opcion == 2:
        crsr.execute("INSERT INTO sala (personalM_rut, paciente_rut, fecha) VALUES (%s, %s, %s)", (rgtr[0], rgtr[1], rgtr[2]))
        dbuci.commit()
        response = {"respuesta":"Se le ha asignado un Personal Medico al Paciente exitosamente."}
        sendT(sckt, srv, json.dumps(response))
    elif opcion == 3:
        crsr.execute("INSERT INTO pasillo (u_paciente_RUT, tipo, fechaInicio, tiempoUso, estado ) VALUES (%s, 'respirador', %s, %s, %s)", (rgtr[0],rgtr[1],rgtr[2],rgtr[3]))
        dbuci.commit()
        response = {"respuesta":"El respirador ha sido asginado exitosamente."}
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
        print(mT)
        if nS == srv:
            l = []
            mTloads = json.loads(mT)
            print(mTloads["opcion"])
            if mTloads["opcion"] == 1:
                l.append(mTloads["id_equipoMedico"])
                l.append(mTloads["u_paciente_RUT"])
                l.append(mTloads["fechaInicio"])
                l.append(mTloads["tiempoUso"])
                l.append(mTloads["estado"])
            elif mTloads["opcion"] == 2:
                l.append(mTloads["personalM_rut"])
                l.append(mTloads["paciente_rut"])
                l.append(mTloads["fecha"])
            elif mTloads["opcion"] == 3:
                l.append(mTloads["id_equipoMedico"])
                l.append(mTloads["u_paciente_RUT"])
                l.append(mTloads["fechaInicio"])
                l.append(mTloads["tiempoUso"])
                l.append(mTloads["estado"])
            asiP(opcion = mTloads["opcion"], rgtr = l)
        else:
            response = {"respuesta":"servicio incorrecto"}
            sendT(sckt, srv, json.dumps(response))

    print('Se cierra socket')
    sckt.close()