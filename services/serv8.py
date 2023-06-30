import socket
import utils
from utils import update_componente

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)

sock.connect(server_address)

message = b"00100sinitserv8"

sock.send(message)
status = sock.recv(4096)[10:12].decode('UTF-8')
print(status)
if (status == 'OK'):
    print('Servicio update_componente iniciado de forma correcta\n')
    while True:
        received_message = sock.recv(4096).decode('UTF-8')
        print(received_message)
        client_id = received_message[5:10]
        data = eval(received_message[10:])
        ans = update_componente(
            id_componente=data['id'],
            nombre=data['nombre'],
            estado=data['estado'],
            marca=data['marca'],
            modelo=data['modelo'],
            costo=data['costo'],
            id_maquinaria=data['id_maquinaria']
        )
        response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)
