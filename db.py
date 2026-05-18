import mysql.connector

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "ekthasql"
DB_NAME = "cookwithsnap"

def _base_connection():
    """
    Connection without specifying database.
    Used for creating the database on first run.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ekthasql",
    )

def get_connection():
    """
    Normal connection to the app database.
    Assumes init_db() has already created it (called on import below).
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ekthasql",
        database="cookwithsnap",
    )

def init_db():
    """
    Create the database and recipes table if they don't exist.
    This makes the 'Save Recipe' button work without manual SQL setup.
    """
    # 1) Ensure database exists
    conn = _base_connection()
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS snaptocook")
    cursor.close()
    conn.close()

    # 2) Ensure recipes table exists inside that database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS recipes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )
    conn.commit()
    cursor.close()
    conn.close()

def save_recipe(title, ingredients, instructions):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO recipes (title, ingredients, instructions)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (
            title,
            ", ".join(ingredients),
            "\n".join(instructions)
        ))

        conn.commit()
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print("DB ERROR:", e)
        return False

def fetch_recipes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, ingredients, instructions
        FROM recipes
        ORDER BY created_at DESC
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def delete_recipe(recipe_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "DELETE FROM recipes WHERE id = %s"
        cursor.execute(query, (recipe_id,))

        conn.commit()
        cursor.close()
        conn.close()

        return True
    except Exception as e:
        print("DELETE ERROR:", e)
        return False

try:
    init_db()
except Exception as e:
    print("DB INIT ERROR:", e)