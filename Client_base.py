import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS customer_data(
                        id SERIAL PRIMARY KEY,
                        first_name VARCHAR,
                        second_name VARCHAR,
                        email VARCHAR unique
                    );
                    """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS customer_phones(    
                        id_customer INTEGER REFERENCES customer_data(id),
                        phone VARCHAR
                    );
                    """)
        conn.commit()

def add_client(conn, id, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO customer_data(id, first_name, second_name, email) VALUES(%s, %s, %s, %s);
                    """, (id, first_name, last_name, email))
        cur.execute("""
                    INSERT INTO customer_phones(id_customer, phone) VALUES(%s, %s);
                    """, (id, phones))
        conn.commit()

def add_phone(conn, id, phone):
    with conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO customer_phones(id_customer, phone) VALUES(%s, %s);
                    """, (id, phone))
        conn.commit()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None, old_phone=None):
    if first_name is not None:
        with conn.cursor() as cur:
            cur.execute("""
                        UPDATE customer_data SET first_name=%s WHERE id=%s;
                        """, (first_name, client_id))
            conn.commit()
    if last_name is not None:
        with conn.cursor() as cur:
            cur.execute("""
                        UPDATE customer_data SET second_name=%s WHERE id=%s;
                        """, (last_name, client_id))
            conn.commit()
    if email is not None:
        with conn.cursor() as cur:
            cur.execute("""
                        UPDATE customer_data SET email=%s WHERE id=%s;
                        """, (email, client_id))
            conn.commit()
    if phones is not None:
        with conn.cursor() as cur:
            cur.execute("""
                        UPDATE customer_phones SET phone=%s WHERE id_customer=%s;
                        """, (phones, client_id))
            conn.commit()

def delete_phone(conn, phone):
    with conn.cursor() as cur:
        cur.execute("""
                    DELETE FROM customer_phones WHERE phone=%s;
                    """, (phone,))

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
                    DELETE FROM customer_phones WHERE id_customer=%s;
                    """, (client_id, ))
        conn.commit()
    with conn.cursor() as cur:
        cur.execute("""
                    DELETE FROM customer_data WHERE id=%s;
                    """, (client_id, ))
        conn.commit()

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT * FROM customer_data
                    WHERE first_name=%s OR second_name=%s OR email=%s OR id=(SELECT id_customer FROM customer_phones WHERE phone=%s);
                    """, (first_name, last_name, email, phone))
        print(cur.fetchall())

if __name__ == "__main__":
    with psycopg2.connect(database="clients_db", user="postgres", password="23092011") as conn:
        create_db(conn)
        # add_client(conn, 1, "Иван", "Иванов", "Ivanov@mail.ru", "8(999)111-11-11")
        # add_client(conn, 2, "Пётр", "Петров", "Petrov@mail.ru")
        # add_client(conn, 3, "Иван", "Сидоров", "Sidorov@mail.ru", "8(999)111-44-44")
        # add_phone(conn, 2, "8(999)111-22-22")
        # add_phone(conn, 2, "8(999)111-33-33")
        # change_client(conn, 2,  email="PetrPetrov@mail.ru", phones="8(999)111-33-34", old_phone="8(999)111-33-33")
        # delete_phone(conn, "8(999)111-22-22")
        # delete_client(conn, 3)
        # find_client(conn, first_name="Иван")
        # find_client(conn, phone="8(999)111-33-34")
    conn.close()