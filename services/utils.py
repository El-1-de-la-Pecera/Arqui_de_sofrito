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
                user text,
                password text,
                type integer DEFAULT 0
            )
            '''
    )

    c.execute(
        '''CREATE TABLE IF NOT EXISTS productos
            (
                id integer PRIMARY KEY AUTOINCREMENT,
                nombre text,
                estado text,
                costo integer,
                fecha_ingreso datetime DEFAULT CURRENT_DATE,
                fecha_salida datetime
            )
        '''
    )

    c.execute(
        '''CREATE TABLE IF NOT EXISTS utencilios
            (
                id integer PRIMARY KEY AUTOINCREMENT,
                id_producto integer,
                nombre text,
                estado text,
                marca text,
                modelo text,
                costo integer,
                fecha_ingreso datetime DEFAULT CURRENT_DATE,
                fecha_salida datetime,
                FOREIGN KEY (id_producto) REFERENCES productos (id)
            )
        '''
    )

    c.execute(
        '''CREATE TABLE IF NOT EXISTS historial_utencilios
            (
                id integer PRIMARY KEY AUTOINCREMENT,
                id_utencilios integer,
                id_producto integer,
                nombre text,
                estado text,
                marca text,
                modelo text,
                costo integer,
                fecha_ingreso datetime,
                fecha_salida datetime,
                fecha_modificacion datetime DEFAULT CURRENT_DATE,
                FOREIGN KEY (id_utencilios) REFERENCES utencilios (id),
                FOREIGN KEY (id_producto) REFERENCES productos (id)
            )
        '''
    )

    c.execute(
        '''CREATE TRIGGER IF NOT EXISTS update_utencilios
            AFTER UPDATE ON utencilios
            BEGIN
                INSERT INTO historial_utencilios 
                (
                    id_utencilios, 
                    id_producto, 
                    nombre, 
                    estado, 
                    marca, 
                    modelo, 
                    costo, 
                    fecha_ingreso, 
                    fecha_salida                    
                )
                VALUES (
                    OLD.id, 
                    OLD.id_producto, 
                    OLD.nombre, 
                    OLD.estado, 
                    OLD.marca,
                    OLD.modelo, 
                    OLD.costo, 
                    OLD.fecha_ingreso, 
                    OLD.fecha_salida
                );
            END
        '''
    )

    c.execute(
        '''CREATE TRIGGER IF NOT EXISTS insert_utencilios
            AFTER INSERT ON utencilios
            BEGIN
                INSERT INTO historial_utencilios (id_utencilios, id_producto, nombre, estado, marca, modelo, costo, fecha_ingreso, fecha_salida)
                VALUES (NEW.id, NEW.id_producto, NEW.nombre, NEW.estado, NEW.marca,
                        NEW.modelo, NEW.costo, NEW.fecha_ingreso, NEW.fecha_salida);
            END
        '''
    )

    c.execute(
        '''CREATE TABLE IF NOT EXISTS historial_productos
            (
                id integer PRIMARY KEY AUTOINCREMENT,
                id_producto integer,
                nombre text,
                estado text,
                costo integer,
                fecha_ingreso datetime,
                fecha_salida datetime,
                fecha_modificacion datetime DEFAULT CURRENT_DATE,
                FOREIGN KEY (id_producto) REFERENCES productos (id)
            )'''
    )

    c.execute(
        '''CREATE TRIGGER IF NOT EXISTS update_producto
            AFTER UPDATE ON productos
            BEGIN
                INSERT INTO historial_productos (id_producto, nombre, estado, costo, fecha_ingreso, fecha_salida)
                VALUES (OLD.id, OLD.nombre, OLD.estado, OLD.costo,
                        OLD.fecha_ingreso, OLD.fecha_salida);
            END
        '''
    )

    c.execute(
        '''CREATE TRIGGER IF NOT EXISTS insert_producto
            AFTER INSERT ON productos
            BEGIN
                INSERT INTO historial_productos (id_producto, nombre, estado, costo, fecha_ingreso, fecha_salida)
                VALUES (NEW.id, NEW.nombre, NEW.estado, NEW.costo,
                        NEW.fecha_ingreso, NEW.fecha_salida);
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


def insert_user(email, password,  type):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''INSERT INTO users(email, password,  type) VALUES(?, ?, ?, ?, ?)''',
        (email,  password,  type)
    )

    conn.commit()
    conn.close()


def insert_producto(nombre, estado, costo):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''INSERT INTO productos(nombre, estado, costo) VALUES(?, ?, ?)''',
        (nombre, estado, costo)
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


def update_producto(id_producto, nombre, estado, costo):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''UPDATE productos SET nombre= ?, estado= ?, costo= ? WHERE id= ?''',
        (nombre, estado, costo, id_producto)
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


def insert_utencilios(id_producto, nombre, estado, marca, modelo, costo):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''INSERT INTO utencilios(id_producto, nombre, estado, marca, modelo, costo) VALUES(?, ?, ?, ?, ?, ?)''',
        (id_producto, nombre, estado, marca, modelo, costo)
    )

    conn.commit()
    conn.close()
    return c.rowcount


def consulta_utencilios(id_utencilios=''):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    if id_utencilios == '':
        c.execute('''SELECT * FROM utencilios''')
    else:
        c.execute(
            '''SELECT * FROM utencilios WHERE id= ?''', (id_utencilios,))
    res = c.fetchall()
    conn.commit()
    conn.close()
    return res


def consulta_historial_utencilios(id_utencilios=''):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    print(id_utencilios)
    c.execute(
        '''SELECT * FROM historial_utencilios WHERE id_utencilios= ?''', (id_utencilios,))
    res = c.fetchall()
    conn.commit()
    conn.close()
    return res


def update_utencilios(
    id_utencilios,
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
        '''UPDATE utencilios
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
            id_utencilios
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
    insert_user('admin@email.com', 'admin', 'admin',
                '12345678-9', 0)  # admin (type 0)
    insert_producto('producto1', 'nuevo', 100)
    insert_producto('producto2', 'casi nuevo', 200)
    insert_producto('producto3', 'usado', 50)
    insert_utencilios(1, 'utencilios2', 'nuevo', 'marca2', 'modelo2', 20)
    insert_utencilios(1, 'utencilios3', 'nuevo', 'marca3', 'modelo3', 30)
    insert_utencilios(2, 'utencilios4', 'nuevo', 'marca4', 'modelo4', 40)
    insert_utencilios(2, 'utencilios5', 'nuevo', 'marca5', 'modelo5', 50)
    insert_utencilios(2, 'utencilios6', 'nuevo', 'marca6', 'modelo6', 60)
    insert_utencilios(3, 'utencilios7', 'nuevo', 'marca7', 'modelo7', 70)
