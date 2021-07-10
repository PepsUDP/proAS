import socket, sys, json
from os import system, name
from services.db_uci import dbuci

#Armado y envío transacción
def sendT(sckt, srv, arg):
    if len(srv) < 5 or len(arg) < 1:
        print("Revisar argumentos")
        return
    lT = str(len(arg) + 5)
    while len(lT) < 5:
        lT = '0' + lT
    T = lT + srv + arg
    sckt.sendall(T.encode())

#Comunicación bus
def listenB(sckt):
    amntRcvd = 0
    sT = None
    msgT = ''

    while True:
        data = sckt.recv(4096)
        if amntRcvd == 0:
            sT = int(data[:5].decode())
            nameSrv = data[5:10].decode()
            msgT = msgT + data[10:].decode()
            amntRcvd = amntRcvd + len(data)-5
        else:
            msgT = msgT + data.decode()
            amntRcvd = amntRcvd + len(data)
        if amntRcvd >= sT:
            break
    return nameSrv, msgT

#Registrar servicio
def registerS(sckt, srv):
    sendT(sckt, 'sinit', srv)
    nS, mT = listenB(sckt)
    if nS == 'sinit' and mT[:2] == 'OK':
        print('Servicio activado exitosamente.')
    else:
        print('No ha sido posible activar el servicio: ', srv, '.')