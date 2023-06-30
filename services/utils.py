import sqlite3
import os


def str_bus_format(data, service_name=''):
    total_digits = 5
    transformed_data = str(data)
    transformed_data_len = len(transformed_data)
    digits_left = total_digits - len(str(transformed_data_len))
    str_data_lenght = ''
    for i in range(digits_left):
        str_data_lenght += '0'
    str_data_lenght += str(transformed_data_len) + \
        service_name+transformed_data
    return str_data_lenght


def create_tables():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS users
            (
                ID integer AUTOINCREMENT PRIMARY KEY,
                usuario text,
                clave text,
                tipo integer DEFAULT 0
            )
            '''
    )

    c.execute(
        '''CREATE TABLE IF NOT EXISTS productos
            (
                SKU text PRIMARY KEY AUTOINCREMENT,
                nombre text,
                precio integer,
                stock integer,
                categoria text
            )
        '''
    )

    c.execute(
        '''CREATE TABLE IF NOT EXISTS utensilios
            (
                id integer PRIMARY KEY AUTOINCREMENT,
                nombre text,
                estado text,
                costo integer
            )
        '''
    )

    c.execute(
        '''CREATE TABLE IF NOT EXISTS historial_utensilios
            (
                id integer PRIMARY KEY AUTOINCREMENT,
                id_utensilios integer,
                nombre text,
                estado text,
                costo integer,
                fecha_modificacion datetime DEFAULT CURRENT_DATE,
                FOREIGN KEY (id_utensilios) REFERENCES utensilios (id),
            )
        '''
    )

    c.execute(
        '''CREATE TRIGGER IF NOT EXISTS update_utensilios
            AFTER UPDATE ON utensilios
            BEGIN
                INSERT INTO historial_utensilios 
                (
                    id_utensilios, 
                    nombre, 
                    estado, 
                    costo
                )
                VALUES (
                    OLD.id, 
                    OLD.nombre, 
                    OLD.estado, 
                    OLD.costo
                );
            END
        '''
    )

    c.execute(
        '''CREATE TRIGGER IF NOT EXISTS insert_utensilios
            AFTER INSERT ON utensilios
            BEGIN
                INSERT INTO historial_utensilios (id_utensilios, nombre, estado, costo)
                VALUES (NEW.id, NEW.nombre, NEW.estado, NEW.costo );
            END
        '''
    )

    c.execute(
        '''CREATE TABLE IF NOT EXISTS historial_productos
            (
                SKU text PRIMARY KEY,
                nombre text,
                precio integer,
                stock integer,
                categoria text,
                fecha_modificacion datetime DEFAULT CURRENT_DATE,
                FOREIGN KEY (id_producto) REFERENCES productos (id)
            )'''
    )

    c.execute(
        '''CREATE TRIGGER IF NOT EXISTS update_producto
            AFTER UPDATE ON productos
            BEGIN
                INSERT INTO historial_productos (SKU, nombre, precio, stock, categoria)
                VALUES (OLD.SKU, OLD.nombre, OLD.precio, OLD.stock, OLD.categoria);
            END
        '''
    )

    c.execute(
        '''CREATE TRIGGER IF NOT EXISTS insert_producto
            AFTER INSERT ON productos
            BEGIN
                INSERT INTO historial_productos (SKU, nombre, precio, stock, categoria)
                VALUES (NEW.SKU, NEW.nombre, NEW.precio, NEW.stock,NEW.cateogria);
            END
        '''
    )

    conn.commit()
    conn.close()


def remove_db():
    try:
        os.remove('db.sqlite3')
    except:
        pass


def insert_usuario(usuario,  clave,  tipo):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''INSERT INTO users(usuario, clave,  tipo) VALUES(?, ?, ?,)''',
        (usuario,  clave,  tipo)
    )

    conn.commit()
    conn.close()


def insert_producto(SKU, nombre, precio, stock, categoria):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''INSERT INTO productos(SKU, nombre, precio, stock, categoria) VALUES(?, ?,? ,?, ?)''',
        (SKU, nombre, precio, stock, categoria)
    )

    conn.commit()
    conn.close()


def consulta_producto(SKU=''):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    if SKU == '':
        c.execute('''SELECT * FROM productos''')
    else:
        c.execute(
            '''SELECT * FROM productos WHERE SKU= ?''', (SKU,))
    res = c.fetchall()
    conn.commit()
    conn.close()
    return res


def update_producto(SKU,  nombre, precio, stock, categoria):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''UPDATE productos SET nombre= ?, precio= ?, stock= ?, categoria=? WHERE id= ?''',
        ( nombre, precio, stock, categoria, SKU)
    )

    conn.commit()
    conn.close()
    return c.rowcount


def delete_producto(SKU):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''UPDATE productos WHERE SKU= ?''',
        (SKU)
    )

    conn.commit()
    conn.close()
    return c.rowcount


def insert_utensilios(nombre, estado, costo):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''INSERT INTO utensilios( nombre, estado, costo) VALUES(?, ?, ?)''',
        ( nombre, estado, costo)
    )

    conn.commit()
    conn.close()
    return c.rowcount


def consulta_utensilios(id_utensilios=''):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    if id_utensilios == '':
        c.execute('''SELECT * FROM utensilios''')
    else:
        c.execute(
            '''SELECT * FROM utensilios WHERE id= ?''', (id_utensilios,))
    res = c.fetchall()
    conn.commit()
    conn.close()
    return res


def consulta_historial_utensilios(id_utensilios=''):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    print(id_utensilios)
    c.execute(
        '''SELECT * FROM historial_utensilios WHERE id_utensilios= ?''', (id_utensilios,))
    res = c.fetchall()
    conn.commit()
    conn.close()
    return res


def update_utensilios(
    id_utensilios,
    nombre,
    estado,
    costo
):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''UPDATE utensilios
        SET nombre= ?,
            estado= ?,
            costo= ?
        WHERE id= ?''',
        (
            nombre,
            estado,
            costo,
            id_utensilios
        )
    )

    conn.commit()
    conn.close()
    return c.rowcount


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def w_print(*text):
    print(bcolors.WARNING, *text, bcolors.ENDC)


def g_print(*text):
    print(bcolors.OKGREEN, *text, bcolors.ENDC)


def f_print(*text):
    print(bcolors.FAIL, *text, bcolors.ENDC)


def b_print(*text):
    print(bcolors.OKBLUE, *text, bcolors.ENDC)


def h_print(*text):
    print(bcolors.HEADER, *text, bcolors.ENDC)


def u_print(*text):
    print(bcolors.UNDERLINE, *text, bcolors.ENDC)


if __name__ == '__main__':
    remove_db()
    create_tables()
    insert_usuario( 'admin', 'admin', 0)  # admin (tipo 0)
    insert_producto('AIDNSFV', 'producto1', 100, 54, 'categoria1')
    insert_producto('AIDNSFV2', 'producto2', 200, 54, 'categoria2')
    insert_producto('AIDNSFV3', 'producto3', 300, 54, 'categoria3')
    insert_producto('AIDNSFV4', 'producto4', 400, 54, 'categoria4')
    insert_utensilios('utensilios2', 'nuevo',  20)
    insert_utensilios( 'utensilios3', 'usado', 30)
    insert_utensilios( 'utensilios4', 'nuevo', 40)
    insert_utensilios( 'utensilios5', 'nuevo',  50)
    insert_utensilios( 'utensilios6', 'nuevo',  60)
    insert_utensilios('utensilios7', 'nuevo',  70)
