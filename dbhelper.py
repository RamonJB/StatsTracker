import sqlite3
from gamestats import GameStats


class DBHelper:

    def __init__(self):
        # Connect to ':memory:' for testing.
        self.db_connection = sqlite3.connect('stats.db')
        self.db_cursor = self.db_connection.cursor()


    def create_table(self):
        try:
            self.db_cursor.execute("""CREATE TABLE stats (
                                game_id INTEGER PRIMARY KEY,
                                date text,
                                game text,
                                game_type text,
                                game_mode text,
                                game_result text,
                                frags integer,
                                deaths integer,
                                assists integer,
                                fd_ratio real)""")
            print("Table created.")
        except:
            print("Table already created.")
            pass


    def insert_stats(self, stats):
        with self.db_connection:
            self.db_cursor.execute("""INSERT INTO stats VALUES (
                :game_id, 
                :date, 
                :game, 
                :game_type, 
                :game_mode, 
                :game_result, 
                :frags, 
                :deaths, 
                :assists, 
                :fd_ratio)""", 
            {
                'game_id': None, 
                'date': stats.date, 
                'game': stats.game, 
                'game_type': stats.game_type,
                'game_mode': stats.variant,
                'game_result': stats.game_result,
                'frags': stats.frags, 
                'deaths': stats.deaths, 
                'assists': stats.assists,
                'fd_ratio': stats.fd_ratio  
            })


    def get_stats_by_id(self, id):
        self.db_cursor.execute("SELECT * FROM STATS WHERE game_id = :id", {'id': id})
        return self.db_cursor.fetchone()


    def get_all_stats(self):
        self.db_cursor.execute("SELECT * FROM stats")
        return self.db_cursor.fetchall()


    def update_stats(self, stats, id):
        with self.db_connection:
            self.db_cursor.execute("""UPDATE stats 
                        SET date = :date,
                        game = :game, 
                        game_type = :game_type,
                        game_mode = :game_mode,
                        game_result = :game_result,
                        frags = :frags,
                        deaths = :deaths,
                        assists = :assists,
                        fd_ratio = :fd_ratio
                        WHERE game_id = :game_id""",
                        {
                            'game_id': id,
                            'date': stats.date, 
                            'game': stats.game, 
                            'game_type': stats.game_type,
                            'game_mode': stats.variant,
                            'game_result': stats.game_result,
                            'frags': stats.frags, 
                            'deaths': stats.deaths, 
                            'assists': stats.assists,
                            'fd_ratio': stats.fd_ratio  
                        })


    def remove_stats_by_id(self, game_id):
        with self.db_connection:
            self.db_cursor.execute("DELETE from stats WHERE game_id = :game_id",
                        {
                          'game_id': game_id
                        })


    def __enter__(self):
        return self


    def __exit__(self, ext_type, exc_value, traceback):
        self.db_cursor.close()
        if isinstance(exc_value, Exception):
            self.db_connection.rollback()
        else:
            self.db_connection.commit()
        self.db_connection.close()

    
    def __del__(self):
        self.db_connection.close()