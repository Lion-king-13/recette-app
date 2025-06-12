import random
import sqlite3

def create_db_connection(db_name=":memory:"):
    conn = sqlite3.connect(db_name)
    return conn

def create_tables(conn):
    create_table_entree(conn)
    create_table_plat(conn)
    create_table_dessert(conn)
    conn.commit()

def create_table_entree(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS entree (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        nombre_de_personne INT,
        temps_preparation INT,
        ingredients TEXT,
        instructions TEXT
    )    
    """)

def create_table_plat(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS plat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        nombre_de_personne INT,
        temps_preparation INT,
        ingredients TEXT,
        instructions TEXT
    )    
    """)

def create_table_dessert(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS dessert (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        nombre_de_personne INT,
        temps_preparation INT,
        ingredients TEXT,
        instructions TEXT
    )    
    """)

def add_recipe(conn, table, nom, nombre_de_personne, temps_preparation, ingredients, instructions):
    if table not in ["entree", "plat", "dessert"]:
        raise ValueError(f"Table inconnue : {table}")

    conn.execute(f"""
        INSERT INTO {table} (nom, nombre_de_personne, temps_preparation, ingredients, instructions)
        VALUES (?, ?, ?, ?, ?)
    """, (nom, nombre_de_personne, temps_preparation, ingredients, instructions))
    conn.commit()

def get_recipes_by_category(conn, category):
    if category not in ["entree", "plat", "dessert"]:
        raise ValueError(f"Catégorie inconnue : {category}")

    cursor = conn.execute(f"""
        SELECT id, nom, nombre_de_personne, temps_preparation, ingredients, instructions
        FROM {category}
    """)
    return cursor.fetchall()

def get_random_recipe(conn):
    tables = ["entree", "plat", "dessert"]
    available_tables = []

    for table in tables:
        cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
        if cursor.fetchone()[0] > 0:
            available_tables.append(table)

    if not available_tables:
        return None

    selected_table = random.choice(available_tables)
    cursor = conn.execute(f"""
        SELECT id, nom, nombre_de_personne, temps_preparation, ingredients, instructions
        FROM {selected_table}
        ORDER BY RANDOM()
    """)
    return cursor.fetchone()

def delete_recipe(conn, table, recipe_id):
    if table not in ["entree", "plat", "dessert"]:
        raise ValueError(f"Table inconnue : {table}")

    conn.execute(f"DELETE FROM {table} WHERE id = ?", (recipe_id,))
    conn.commit()
