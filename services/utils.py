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
                rut text PRIMARY KEY,
                email text,
                name text,
                password text,
                type integer DEFAULT 0
            )
            '''
    )

    c.execute(
        '''CREATE TABLE IF NOT EXISTS maquinarias
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
        '''CREATE TABLE IF NOT EXISTS componentes
            (
                id integer PRIMARY KEY AUTOINCREMENT,
                id_maquinaria integer,
                nombre text,
                estado text,
                marca text,
                modelo text,
                costo integer,
                fecha_ingreso datetime DEFAULT CURRENT_DATE,
                fecha_salida datetime,
                FOREIGN KEY (id_maquinaria) REFERENCES maquinarias (id)
            )
        '''
    )

    c.execute(
        '''CREATE TABLE IF NOT EXISTS historial_componentes
            (
                id integer PRIMARY KEY AUTOINCREMENT,
                id_componente integer,
                id_maquinaria integer,
                nombre text,
                estado text,
                marca text,
                modelo text,
                costo integer,
                fecha_ingreso datetime,
                fecha_salida datetime,
                fecha_modificacion datetime DEFAULT CURRENT_DATE,
                FOREIGN KEY (id_componente) REFERENCES componentes (id),
                FOREIGN KEY (id_maquinaria) REFERENCES maquinarias (id)
            )
        '''
    )

    c.execute(
        '''CREATE TRIGGER IF NOT EXISTS update_componente
            AFTER UPDATE ON componentes
            BEGIN
                INSERT INTO historial_componentes 
                (
                    id_componente, 
                    id_maquinaria, 
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
                    OLD.id_maquinaria, 
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
        '''CREATE TRIGGER IF NOT EXISTS insert_componente
            AFTER INSERT ON componentes
            BEGIN
                INSERT INTO historial_componentes (id_componente, id_maquinaria, nombre, estado, marca, modelo, costo, fecha_ingreso, fecha_salida)
                VALUES (NEW.id, NEW.id_maquinaria, NEW.nombre, NEW.estado, NEW.marca,
                        NEW.modelo, NEW.costo, NEW.fecha_ingreso, NEW.fecha_salida);
            END
        '''
    )

    c.execute(
        '''CREATE TABLE IF NOT EXISTS historial_maquinarias
            (
                id integer PRIMARY KEY AUTOINCREMENT,
                id_maquinaria integer,
                nombre text,
                estado text,
                costo integer,
                fecha_ingreso datetime,
                fecha_salida datetime,
                fecha_modificacion datetime DEFAULT CURRENT_DATE,
                FOREIGN KEY (id_maquinaria) REFERENCES maquinarias (id)
            )'''
    )

    c.execute(
        '''CREATE TRIGGER IF NOT EXISTS update_maquinaria
            AFTER UPDATE ON maquinarias
            BEGIN
                INSERT INTO historial_maquinarias (id_maquinaria, nombre, estado, costo, fecha_ingreso, fecha_salida)
                VALUES (OLD.id, OLD.nombre, OLD.estado, OLD.costo,
                        OLD.fecha_ingreso, OLD.fecha_salida);
            END
        '''
    )

    c.execute(
        '''CREATE TRIGGER IF NOT EXISTS insert_maquinaria
            AFTER INSERT ON maquinarias
            BEGIN
                INSERT INTO historial_maquinarias (id_maquinaria, nombre, estado, costo, fecha_ingreso, fecha_salida)
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


def insert_user(email, name, password, rut, type):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''INSERT INTO users(email, name, password, rut, type) VALUES(?, ?, ?, ?, ?)''',
        (email, name, password, rut, type)
    )

    conn.commit()
    conn.close()


def insert_maquinaria(nombre, estado, costo):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''INSERT INTO maquinarias(nombre, estado, costo) VALUES(?, ?, ?)''',
        (nombre, estado, costo)
    )

    conn.commit()
    conn.close()


def consulta_maquinaria(id_maquinaria=''):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    if id_maquinaria == '':
        c.execute('''SELECT * FROM maquinarias''')
    else:
        c.execute(
            '''SELECT * FROM maquinarias WHERE id= ?''', (id_maquinaria,))
    res = c.fetchall()
    conn.commit()
    conn.close()
    return res


def update_maquinaria(id_maquinaria, nombre, estado, costo):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''UPDATE maquinarias SET nombre= ?, estado= ?, costo= ? WHERE id= ?''',
        (nombre, estado, costo, id_maquinaria)
    )

    conn.commit()
    conn.close()
    return c.rowcount


def delete_maquinaria(id_maquinaria):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''UPDATE maquinarias SET fecha_salida=CURRENT_DATE WHERE id= ?''',
        (id_maquinaria)
    )

    conn.commit()
    conn.close()
    return c.rowcount


def insert_componente(id_maquinaria, nombre, estado, marca, modelo, costo):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''INSERT INTO componentes(id_maquinaria, nombre, estado, marca, modelo, costo) VALUES(?, ?, ?, ?, ?, ?)''',
        (id_maquinaria, nombre, estado, marca, modelo, costo)
    )

    conn.commit()
    conn.close()
    return c.rowcount


def consulta_componente(id_componente=''):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    if id_componente == '':
        c.execute('''SELECT * FROM componentes''')
    else:
        c.execute(
            '''SELECT * FROM componentes WHERE id= ?''', (id_componente,))
    res = c.fetchall()
    conn.commit()
    conn.close()
    return res


def consulta_historial_componente(id_componente=''):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    print(id_componente)
    c.execute(
        '''SELECT * FROM historial_componentes WHERE id_componente= ?''', (id_componente,))
    res = c.fetchall()
    conn.commit()
    conn.close()
    return res


def update_componente(
    id_componente,
    id_maquinaria,
    nombre,
    estado,
    marca,
    modelo,
    costo
):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''UPDATE componentes
        SET id_maquinaria= ?,
            nombre= ?,
            estado= ?,
            marca= ?,
            modelo= ?,
            costo= ?
        WHERE id= ?''',
        (
            id_maquinaria,
            nombre,
            estado,
            marca,
            modelo,
            costo,
            id_componente
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
    insert_maquinaria('maquinaria1', 'nuevo', 100)
    insert_maquinaria('maquinaria2', 'casi nuevo', 200)
    insert_maquinaria('maquinaria3', 'usado', 50)
    insert_componente(1, 'componente2', 'nuevo', 'marca2', 'modelo2', 20)
    insert_componente(1, 'componente3', 'nuevo', 'marca3', 'modelo3', 30)
    insert_componente(2, 'componente4', 'nuevo', 'marca4', 'modelo4', 40)
    insert_componente(2, 'componente5', 'nuevo', 'marca5', 'modelo5', 50)
    insert_componente(2, 'componente6', 'nuevo', 'marca6', 'modelo6', 60)
    insert_componente(3, 'componente7', 'nuevo', 'marca7', 'modelo7', 70)
