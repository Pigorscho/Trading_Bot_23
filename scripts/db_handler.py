import sqlite3

sql_add_player = '''
INSERT OR IGNORE INTO player_blacklist
VALUES(
    "{}", 0
)
'''

sql_is_listed = '''
SELECT *
FROM player_blacklist
WHERE name = "{}"
'''

sql_increment = '''
UPDATE player_blacklist
SET counter = "{}"
WHERE name = "{}"
'''

class DBHandler:
    def __init__(self):
        self.conn = sqlite3.connect(r'db\trading_stats.db')
        self.db = self.conn.cursor()

    def execute(self, param):
        print(f'sql: {param}')
        return self.db.execute(param)

    def add_player(self, name):
        self.execute(sql_add_player.format(name))
        self.conn.commit()

    def is_listed(self, player_name) -> bool:
        is_listed = False
        result = self.execute(sql_is_listed.format(player_name)).fetchone()
        print(f'{result = }')
        if result:
            incremented = False
            player, counter = result
            if counter == 2:
                is_listed = True
            else:
                incremented = True
                counter += 1
            if incremented:
                self.execute(sql_increment.format(counter, player_name))
                self.conn.commit()
        self.conn.close()
        return is_listed


if __name__ == '__main__':
    import os
    os.chdir(r'..')
    handle = DBHandler()
    """
    # refresh
    # handle.execute('DROP TABLE IF EXISTS player_blacklist')
    # handle.execute('''
    #     CREATE TABLE IF NOT EXISTS player_blacklist(
    #         name STR PRIMARY KEY,
    #         counter INT DEFAULT 0
    #     )
    # ''')
    """
    # handle.add_player("Piero Hincapié")
    print(handle.is_listed("Piero Hincapié"))



