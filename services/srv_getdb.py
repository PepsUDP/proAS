import socket, json
from db_uci import dbuci
from comunicacion import sendT, listenB, registerS
srv = 'ccddb'

# Obtener datos
def getData(opcion):
    crsr = dbuci.cursor()
    print(opcion)
    fetched = None
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
    if fetched:
        response = {"respuesta":fetched}
        sendT(sckt, srv, json.loads(response))
    else:
        print("No sacó nada")

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
        msg = json.loads(mT[12:])
        print("msg", msg)
        print("msg:opcion",msg["opcion"])
        if nS == srv:
            getData(opcion=json.loads(mT))
        else:
            response = {"respuesta":"servicio incorrecto"}
            sendT(sckt, srv, json.dumps(response))

    print('Se cierra socket')
    sckt.close()