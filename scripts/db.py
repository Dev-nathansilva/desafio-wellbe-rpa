import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="wellbe_rpa"
    )


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            movie_name VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            search_term VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY uq_movie_search (movie_name, search_term)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


def insert_movie(movie_name, description, search_term="Avengers"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT IGNORE INTO movies (movie_name, description, search_term)
        VALUES (%s, %s, %s)
    """, (movie_name, description, search_term))

    conn.commit()
    cursor.close()
    conn.close()


def movie_exists(movie_name, search_term="Avengers"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM movies
        WHERE movie_name = %s AND search_term = %s
    """, (movie_name, search_term))

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return count > 0