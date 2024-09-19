import sqlite3


def logger(statement):
    print(f"""
--------------------------------------------------
Executing:
{statement}
--------------------------------------------------
""")


class DataBase:

    def __init__(self, path_to_db='cities_game.db'):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self,
                sql: str,
                parameters: tuple = (),
                fetchone: bool = False,
                fetchall: bool = False,
                commit=False
                ):
        conn = self.connection  # открываем соединение
        conn.set_trace_callback(logger)
        cursor = conn.cursor()  # устанавливаем курсор
        data = None

        cursor.execute(sql, parameters)  # Вызываем полученные SQL - команду

        if commit:
            conn.commit()  # сохранить изменения в БД
        if fetchone:  # выгрузить одно значение (например только id) из БД в Python
            data = cursor.fetchone()
        if fetchall:  # выгрузить все данные из БД в Python
            data = cursor.fetchall()
        conn.close()
        return data

    def create_table_games(self):
        sql_query = """
        CREATE TABLE IF NOT EXISTS games (
        chat_id INT, 
        current_turn TEXT CHECK(current_turn IN ('player', 'bot')) NOT NULL,  
        difficulty TEXT CHECK(difficulty IN ('easy', 'medium', 'hard')) NOT NULL,
        is_active INTEGER NOT NULL DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        city_count INT DEFAULT 0
        );
        """
        self.execute(sql=sql_query, commit=True)

    def create_table_moves(self):
        sql_query = """
        CREATE TABLE IF NOT EXISTS moves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER NOT NULL,
        player_type TEXT CHECK(player_type IN ('player', 'bot')) NOT NULL,
        city TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (chat_id) REFERENCES games(chat_id),
        UNIQUE (chat_id, city)
        );
        """
        self.execute(sql=sql_query, commit=True)

    def create_new_game(self, chat_id, difficulty):
        sql_query = """
        INSERT INTO games (
        chat_id, current_turn, difficulty, is_active, created_at, city_count)
        VALUES (?, 'player', ?, 1, DATETIME(CURRENT_TIMESTAMP, '+3 hours'), 0);
        """
        params = (chat_id, difficulty)
        self.execute(sql=sql_query, commit=True, parameters=params)

    def create_new_move(self, chat_id, player_type, city):
        sql_query = """
        INSERT INTO moves (
        chat_id, player_type, city, timestamp)
        VALUES (?, ?, ?, DATETIME(CURRENT_TIMESTAMP, '+3 hours'));
        """
        params = (chat_id, player_type, city)
        self.execute(sql=sql_query, commit=True, parameters=params)

        sql_query_1 = """
        UPDATE games
        SET current_turn = ?, city_count = city_count + 1
        WHERE chat_id = ? AND created_at = (
        SELECT created_at 
        FROM games 
        WHERE chat_id = ? 
        ORDER BY created_at DESC 
        LIMIT 1
    );
        """
        params1 = ('bot' if player_type == 'player' else 'player', chat_id, chat_id)
        self.execute(sql=sql_query_1, commit=True, parameters=params1)

    def is_game_active(self, chat_id):
        result = self.execute(sql="SELECT is_active FROM games WHERE chat_id = ? ORDER BY created_at DESC LIMIT 1",
                              parameters=(chat_id,), fetchone=True)
        if result:
            return result[0] == 1
        return False

    def is_city_used(self, chat_id, city):
        city_variants = [city, city.replace("-", " "), city.replace(" ", "-")]

        sql = """
            SELECT 1 FROM moves 
            WHERE chat_id = ? 
            AND (city = ? OR city = ? OR city = ?)
        """

        return self.execute(sql=sql, parameters=(chat_id, city_variants[0], city_variants[1], city_variants[2]),
                            fetchone=True) is not None

    def end_game(self, chat_id):
        sql_query = """
        UPDATE games
        SET is_active = 0
        WHERE chat_id = ?;
        """
        self.execute(sql=sql_query, parameters=(chat_id,), commit=True)

        sql_query_moves = """
        DELETE FROM moves
        WHERE chat_id = ?;
        """
        self.execute(sql=sql_query_moves, parameters=(chat_id,), commit=True)

    def get_game_difficulty(self, chat_id):
        sql_query = """
        SELECT difficulty FROM games
        WHERE chat_id = ? AND is_active = 1
        LIMIT 1;
        """
        return self.execute(sql=sql_query, parameters=(chat_id,), fetchone=True)[0]

    def get_game_current_turn(self, chat_id):
        sql_query = """
        SELECT current_turn FROM games
        WHERE chat_id = ? AND is_active = 1
        LIMIT 1;
        """
        return self.execute(sql=sql_query, parameters=(chat_id,), fetchone=True)[0]

    def get_last_bot_city(self, chat_id):
        sql_query = """
           SELECT city
           FROM moves
           WHERE chat_id = ? AND player_type = 'bot'
           ORDER BY timestamp DESC
           LIMIT 1;
           """
        result = self.execute(sql=sql_query, parameters=(chat_id,), fetchone=True)
        return result[0] if result else None

    def get_city_count(self, chat_id):
        sql_query = """
        SELECT city_count FROM games
        WHERE chat_id = ? AND is_active = 1
        ORDER BY created_at DESC
        LIMIT 1;
        """
        result = self.execute(sql=sql_query, parameters=(chat_id,), fetchone=True)
        return result[0] if result else 0

    def get_top_5_games(self, chat_id):
        sql_query = """
        SELECT chat_id, city_count, created_at
        FROM games
        WHERE is_active = 0 AND chat_id = ?
        ORDER BY city_count DESC
        LIMIT 5;
        """
        return self.execute(sql=sql_query, parameters=(chat_id,), fetchall=True)
