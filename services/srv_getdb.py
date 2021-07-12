import socket, json
from db_uci import dbuci
from comunicacion import sendT, listenB, registerS
srv = 'ccddb'

class create_dict(dict):
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value

# Obtener datos
def getData(opcion):
    mydict = create_dict()
    crsr = dbuci.cursor()
    print(opcion)
    fetched = None
    if opcion == 1:
        crsr.execute("SELECT * FROM pasillo;")   
        fetched = crsr.fetchall()
        for row in fetched:
            mydict.add(row[0],({"estado":row[1]}))
    elif opcion == 2:
        crsr.execute("SELECT * FROM sala;")
        fetched = crsr.fetchall()
        for row in fetched:
            mydict.add(row[0],({"cantCamas":row[1],"camasDisp":row[2],"estado":row[3]}))
    elif opcion == 3:
        crsr.execute("SELECT * FROM equipoMedico WHERE tipo='cama';")   
        fetched = crsr.fetchall()
        for row in fetched:
            mydict.add(row[0],({"u_paciente_RUT":row[1],"tipo":row[2],"fechaInicio":str(row[3]),"tiempoUso":row[4],"estado":row[5]}))
    elif opcion == 4:
        crsr.execute("SELECT * FROM paciente;") 
        fetched = crsr.fetchall()
        for row in fetched:
            mydict.add(row[0],({"nombre":row[1],"fechanac":row[2],"edad":row[3],"enfermedad":row[4],"sintomas":row[5],"dieta":row[6],"alergias":row[7],"medicamentos":row[8],"tratamiento":row[9]}))
    elif opcion == 5:
        crsr.execute("SELECT * FROM personalMedico;")
        fetched = crsr.fetchall()
        for row in fetched:
            mydict.add(row[0],({"nombre":row[1],"fechanac":str(row[2]),"especialidad":row[3],"disponible":row[4]}))
    elif opcion == 6:    
        crsr.execute("SELECT * FROM equipoMedico WHERE tipo='respirador';")
        fetched = crsr.fetchall()
        for row in fetched:
            mydict.add(row[0],({"u_paciente_RUT":row[1],"tipo":row[2],"fechaInicio":str(row[3]),"tiempoUso":row[4],"estado":row[5]}))
    if fetched:
        response = json.dumps(mydict, indent=2, sort_keys=True)
        print(response)
        #test = '{' + response[1:-1] + '}'
        #print(test)
        #response = {"respuesta":fetched}
        sendT(sckt, srv, response)
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
        msg = json.loads(mT)
        print("msg", msg)
        print("msg:opcion",msg["opcion"])
        if nS == srv:
            getData(opcion=msg["opcion"])
        else:
            response = {"respuesta":"servicio incorrecto"}
            sendT(sckt, srv, json.dumps(response))

    print('Se cierra socket')
    sckt.close()