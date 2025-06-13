import random
import sqlite3

def create_db(my_db="my_data_base.db"):
    """
        Cette fonction crée une connexion à une base de données SQLite.

        Paramètres :
            my_db (str) : Nom du fichier de la base de données (par défaut : 'my_data_base.db').

        Effet :
            Initialise les variables globales 'conn' (connexion) et 'cursor' (curseur) pour interagir avec la base de données.
        """
    global cursor, conn
    conn = sqlite3.connect(my_db)
    cursor = conn.cursor()

def setup_db():
    """
        Cette fonction configure la base de données en créant les tables nécessaires.

        Effet :
            Appelle create_db() pour établir la connexion et crée les tables pour les entrées, plats et desserts.
            Valide les modifications dans la base de données.
        """
    create_db()
    create_table_entree()
    create_table_plat()
    create_table_dessert()
    conn.commit()

def create_table_entree():
    """
        Cette fonction crée la table 'entree' dans la base de données si elle n'existe pas déjà.

        Effet :
            Crée une table avec les colonnes id, nom, nombre_de_personne, temps_preparation, ingredients et instructions.
        """
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entree (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        nombre_de_personne INT,
        temps_preparation INT,
        ingredients TEXT,
        instructions TEXT
        )    
    """)
def create_table_plat():
    """
        Cette fonction crée la table 'plat' dans la base de données si elle n'existe pas déjà.

        Effet :
            Crée une table avec les colonnes id, nom, nombre_de_personne, temps_preparation, ingredients et instructions.
        """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            nombre_de_personne INT,
            temps_preparation INT,
            ingredients TEXT,
            instructions TEXT
            )    
        """)
def create_table_dessert():
    """
        Cette fonction crée la table 'dessert' dans la base de données si elle n'existe pas déjà.

        Effet :
            Crée une table avec les colonnes id, nom, nombre_de_personne, temps_preparation, ingredients et instructions.
        """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dessert (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            nombre_de_personne INT,
            temps_preparation INT,
            ingredients TEXT,
            instructions TEXT
            )    
        """)

def add_recipe(table, nom, nombre_de_personne, temps_preparation, ingredients, instructions):
    """
        Cette fonction ajoute une recette à la table spécifiée dans la base de données.

        Paramètres :
            table (str) : Nom de la table ('entree', 'plat' ou 'dessert').
            nom (str) : Nom de la recette.
            nombre_de_personne (int) : Nombre de personnes pour la recette.
            temps_preparation (int) : Temps de préparation en minutes.
            ingredients (str) : Liste des ingredients.
            instructions (str) : instructionss de préparation.

        Effet :
            Insère une nouvelle recette dans la table spécifiée et valide les modifications.

        Exception :
            Lève ValueError si la table spécifiée est inconnue.
        """
    if table not in ["entree", "plat", "dessert"]:
        raise ValueError(f"Table inconnue : {table}")

    cursor.execute(f"""
        INSERT INTO {table} (nom, nombre_de_personne, temps_preparation, ingredients, instructions)
        VALUES (?, ?, ?, ?, ?)
    """, (nom, nombre_de_personne, temps_preparation, ingredients, instructions))
    conn.commit()


def get_recipes_by_category(category):
    """
        Cette fonction récupère toutes les recettes d'une catégorie donnée.

        Paramètres :
            category (str) : Nom de la catégorie ('entree', 'plat' ou 'dessert').

        Retourne :
            list : Liste des recettes sous forme de tuples (id, nom, nombre_de_personne, temps_preparation, ingredients, instructions).

        Exception :
            Lève ValueError si la catégorie est inconnue.
        """
    if category not in ["entree", "plat", "dessert"]:
        raise ValueError(f"Catégorie inconnue : {category}")

    cursor.execute(f"SELECT id, nom, nombre_de_personne, temps_preparation, ingredients, instructions FROM {category}")
    return cursor.fetchall()

def get_random_recipe():
    """
        Cette fonction sélectionne une recette aléatoire parmi toutes les tables non vides.

        Retourne :
            tuple : Une recette sous forme (id, nom, nombre_de_personne, temps_preparation, ingredients, instructions),
                    ou None si aucune recette n'est disponible.
        """
    tables = ["entree", "plat", "dessert"]
    available_tables = []

    # On check les tables qui ont des recettes
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        if cursor.fetchone()[0] > 0:
            available_tables.append(table)

    if not available_tables:
        return None  # Si aucune recette disponible

    # On lance le random sur la table et la recette
    selected_table = random.choice(available_tables)
    cursor.execute(
        f"SELECT id, nom, nombre_de_personne, temps_preparation, ingredients, instructions FROM {selected_table} ORDER BY RANDOM()")
    return cursor.fetchone()


def close_db():
    """
        Cette fonction ferme la connexion à la base de données.

        Effet :
            Ferme la connexion SQLite pour libérer les ressources.
        """
    conn.close()

def delete_recipe(table, recipe_id):
    """
        Cette fonction supprime une recette de la table spécifiée en fonction de son ID.

        Paramètres :
            table (str) : Nom de la table ('entree', 'plat' ou 'dessert').
            recipe_id (int) : ID de la recette à supprimer.

        Effet :
            Supprime la recette de la table et valide les modifications.

        Exception :
            Lève ValueError si la table est inconnue.
        """
    if table not in ["entree", "plat", "dessert"]:
        raise ValueError(f"Table inconnue : {table}")

    cursor.execute(f"DELETE FROM {table} WHERE id = ?", (recipe_id,))
    conn.commit()
