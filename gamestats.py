class GameStats:
    def __init__(self, date, game, game_type, variant, game_result, frags, deaths, assists, fd_ratio):
        self.date = date
        self.game = game                # Reach, CE, etc.
        self.game_type = game_type      # 8v8, 4v4, FFA
        self.variant = variant          # Slayer, CTF, etc.
        self.game_result = game_result  # W or L
        self.frags = frags
        self.deaths = deaths
        self.assists = assists
        self.fd_ratio = fd_ratio