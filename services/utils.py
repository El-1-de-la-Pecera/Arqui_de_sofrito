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


def insert_usuario(usuario, clave,  tipo):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''INSERT INTO users(usuario, clave,  tipo) VALUES(?, ?, ?, ?, ?)''',
        (usuario,  clave,  tipo)
    )

    conn.commit()
    conn.close()


def insert_producto(nombre, estado, precio):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''INSERT INTO productos(nombre, estado, precio) VALUES(?, ?, ?)''',
        (nombre, estado, precio)
    )

    conn.commit()
    conn.close()


def consulta_producto(id_producto=''):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    if id_producto == '':
        c.execute('''SELECT * FROM productos''')
    else:
        c.execute(
            '''SELECT * FROM productos WHERE id= ?''', (id_producto,))
    res = c.fetchall()
    conn.commit()
    conn.close()
    return res


def update_producto(id_producto, nombre, estado, precio):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''UPDATE productos SET nombre= ?, estado= ?, precio= ? WHERE id= ?''',
        (nombre, estado, precio, id_producto)
    )

    conn.commit()
    conn.close()
    return c.rowcount


def delete_producto(id_producto):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''UPDATE productos SET fecha_salida=CURRENT_DATE WHERE id= ?''',
        (id_producto)
    )

    conn.commit()
    conn.close()
    return c.rowcount


def insert_utensilios(id_producto, nombre, estado, marca, modelo, costo):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''INSERT INTO utensilios(id_producto, nombre, estado, marca, modelo, costo) VALUES(?, ?, ?, ?, ?, ?)''',
        (id_producto, nombre, estado, marca, modelo, costo)
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
    id_producto,
    nombre,
    estado,
    marca,
    modelo,
    costo
):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''UPDATE utensilios
        SET id_producto= ?,
            nombre= ?,
            estado= ?,
            marca= ?,
            modelo= ?,
            costo= ?
        WHERE id= ?''',
        (
            id_producto,
            nombre,
            estado,
            marca,
            modelo,
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
    insert_usuario('admin@email.com', 'admin', 'admin',
                '12345678-9', 0)  # admin (tipo 0)
    insert_producto('producto1', 'nuevo', 100)
    insert_producto('producto2', 'casi nuevo', 200)
    insert_producto('producto3', 'usado', 50)
    insert_utensilios(1, 'utensilios2', 'nuevo', 'marca2', 'modelo2', 20)
    insert_utensilios(1, 'utensilios3', 'nuevo', 'marca3', 'modelo3', 30)
    insert_utensilios(2, 'utensilios4', 'nuevo', 'marca4', 'modelo4', 40)
    insert_utensilios(2, 'utensilios5', 'nuevo', 'marca5', 'modelo5', 50)
    insert_utensilios(2, 'utensilios6', 'nuevo', 'marca6', 'modelo6', 60)
    insert_utensilios(3, 'utensilios7', 'nuevo', 'marca7', 'modelo7', 70)
