import socket
from services.utils import str_bus_format, w_print, f_print, g_print, h_print, b_print, bcolors

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = ('localhost', 5000)
# sock.connect(server_address)


class App:
    def __init__(self, login_service, services=[]) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 5000)
        self.sock.connect(server_address)
        self.services = services
        self.login_service = login_service

    def send_message(self, data, service_name='g7999'):
        req = str_bus_format(data, service_name).encode('UTF-8')
        self.sock.send(req)
        return self.sock.recv(4096).decode('UTF-8')

    def login(self):
        h_print('\n', '-'*20, 'Login', '-'*20, '\n')
        inputs = {}
        for i in range(len(self.login_service['inputs'])):
            actual_input = self.login_service['inputs'][i]
            key = actual_input['key']
            inputs[key] = input(actual_input['desc'])
        res = self.send_message(inputs, self.login_service['id'])
        return res

    def show_menu(self):
        while True:
            h_print("\n", "-"*20, "Bienvenido", "-"*20, "\n")
            b_print("Menu de opciones:\n")
            print("Opcion 1: {}".format(self.login_service['desc']))
            print("Opcion 0: Salir")
            option = input('Ingrese una opcion: ')
            if option == '1':
                res = self.login()
                data = eval(res[12:])
                if res[10:12] == 'NK':
                    f_print('Servicio no disponible')
                    pass
                elif data == None:
                    f_print('Login fallido')
                    pass
                else:
                    g_print('Login exitoso')
                    break
            elif option == '0':
                return
            else:
                w_print("Opcion no valida")
        self.menu(data[-1])

    def menu(self, type_id):
        while True:
            input(
                f'{bcolors.UNDERLINE}Presione enter para continuar...{bcolors.ENDC}')
            h_print("\n", "-"*20, "Bienvenido", "-"*20, "\n")
            b_print("Menu de opciones:\n")
            available_services = [
                service for service in self.services if type_id in service['user_types']
            ]
            services = {}
            for i in range(len(available_services)):
                actual_service = available_services[i]
                services[f'{i+1}'] = actual_service
                print("Opcion {}: {}".format(i+1, actual_service['desc']))
            print("Opcion 0: Salir")
            option = input('Ingrese una opcion: ')
            if option == '0':
                return
            elif option in services:
                service = services[option]
                inputs = {}
                for i in range(len(service['inputs'])):
                    actual_input = service['inputs'][i]
                    key = actual_input['key']
                    inputs[key] = input(actual_input['desc'])
                res = self.send_message(inputs, service['id'])
                if res[10:12] == 'NK':
                    f_print('Servicio no disponible')
                    pass
                else:
                    service['function'](res)
            else:
                w_print("Opcion no valida")


def display_productos(res):
    data = eval(res[12:])
    productos = [producto for producto in data if not producto[5]]
    if len(productos) == 0:
        f_print('No se encontraron productos')
        return
    g_print('Productos encontradas:')
    for producto in productos:
        b_print('-'*20)
        print('SKU', producto[0])
        print('nombre', producto[1])
        print('precio', producto[2])
        print('stock', producto[3])
        print('categoria', producto[4])


def display_utensilios(res):
    data = eval(res[12:])
    utensilios = [utensilio for utensilio in data if not utensilio[8]]
    if len(data) == 0:
        f_print('No se encontraron utensilios')
        return
    g_print('Utencilios encontrados:')
    for utensilio in utensilios:
        b_print('-'*20)
        print('id', utensilio[0])
        print('nombre', utensilio[1])
        print('estado', utensilio[2])
        print('costo', utensilio[3])



def display_historial_utensilio(res):
    data = eval(res[12:])
    for utensilio in data:
        b_print('-'*20)
        print('id', utensilio[0])
        print('nombre', utensilio[1])
        print('estado', utensilio[2])
        print('costo', utensilio[3])


if __name__ == '__main__':
    app = App(
        login_service={
            'id': 'serv1',
            'desc': 'Iniciar sesión',
            'inputs': [
                {
                    'key': 'usuario',
                    'desc': 'Ingresa tu usuario: '
                },
                {
                    'key': 'clave',
                    'desc': 'Ingresa tu clave: '
                }
            ]
        },
        services=[
            {
                'id': 'serv2',
                'desc': 'Registrar producto',
                'user_types': [0, 1, 2],
                'function': lambda *_: g_print('producto registrado'),
                'inputs': [
                    {
                        'key': 'nombre',
                        'desc': 'Ingresa el nombre del producto: ',
                    },
                    {
                        'key': 'precio',
                        'desc': 'Ingresa el precio del producto: ',
                    },
                    {
                        'key': 'stock',
                        'desc': 'Ingresa el stock del producto: '
                    },
                    {
                        'key': 'categoria',
                        'desc': 'Ingresa el categoria del producto: '
                    }
                ]
            },
            {
                'id': 'serv3',
                'desc': 'Consultar producto',
                'user_types': [0, 1, 2],
                'function': display_productos,
                'inputs': [
                    {
                        'key': 'id',
                        'desc': 'Ingresa el id del producto o vacío para consultar por todas: '
                    }
                ]
            },
            {
                'id': 'serv4',
                'desc': 'Modificar producto',
                'user_types': [0, 1, 2],
                'function': lambda res: g_print('producto modificado') if eval(res[12:]) > 0 else f_print('producto no encontrado'),
                'inputs': [
                    {
                        'key': 'nombre',
                        'desc': 'Ingresa el nombre del producto: ',
                    },
                    {
                        'key': 'precio',
                        'desc': 'Ingresa el precio del producto: ',
                    },
                    {
                        'key': 'stock',
                        'desc': 'Ingresa el stock del producto: '
                    },
                    {
                        'key': 'categoria',
                        'desc': 'Ingresa el categoria del producto: '
                    }
                ]
            },
            {
                'id': 'serv5',
                'desc': 'Eliminar producto',
                'user_types': [0, 1, 2],
                'function': lambda res: g_print('producto eliminado') if eval(res[12:]) > 0 else f_print('producto no encontrado'),
                'inputs': [
                    {
                        'key': 'id',
                        'desc': 'Ingresa el id del producto: '
                    }
                ]
            },
            {
                'id': 'serv6',
                'desc': 'Registrar utensilios',
                'user_types': [0, 1, 2],
                'function': lambda *_: g_print('utensilio registrado'),
                'inputs': [
                    {
                        'key': 'nombre',
                        'desc': 'Ingresa el nombre del utensilio: ',
                    },
                    {
                        'key': 'estado',
                        'desc': 'Ingresa el estado del utensilio: ',
                    },
                    {
                        'key': 'costo',
                        'desc': 'Ingresa el costo del utensilio: '
                    },
                ]
            },
            {
                'id': 'serv7',
                'desc': 'Consultar utensilios',
                'user_types': [0, 1, 2],
                'function': display_utensilios,
                'inputs': [
                    {
                        'key': 'id',
                        'desc': 'Ingresa el id del utensilio o vacío para consultar por todas: '
                    }
                ]
            },
            {
                'id': 'serv8',
                'desc': 'Modificar utensilio',
                'user_types': [0, 1, 2],
                'function': lambda res: g_print('utensilio modificado') if (eval(res[12:])) > 0 else f_print('utensilio no encontrado'),
                'inputs': [
                    {
                        'key': 'id',
                        'desc': 'Ingresa el id del componente: '
                    },
                    {
                        'key': 'nombre',
                        'desc': 'Ingresa el nombre del utensilio: ',
                    },
                    {
                        'key': 'estado',
                        'desc': 'Ingresa el estado del utensilio: ',
                    },
                    {
                        'key': 'costo',
                        'desc': 'Ingresa el costo del utensilio: '
                    },
                ]
            },
            {
                'id': 'serv9',
                'desc': 'Historial de componente',
                'user_types': [0, 1, 2],
                'function': display_historial_utensilio,
                'inputs': [
                    {
                        'key': 'id',
                        'desc': 'Ingresa el id del utensilio: '
                    }
                ]
            }
        ]
    )
    res = app.show_menu()
