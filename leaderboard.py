import sqlite3

class Leaderboard:
    """Is able to create and manipulate the leaderboard table"""
    def __init__(self):
        self.path = "./DB/game.db"

    def set_entry(self,Name,Score,Distance,Kills,Time):
        #creates a new entry
        with sqlite3.connect(self.path) as db:                                                                                              #opens DB
            cursor = db.cursor()
            cursor.execute("INSERT INTO Leaderboard(Name,Score,Distance,Kills,Time) VALUES(?,?,?,?,?)",(Name,Score,Distance,Kills,Time))    #inserts into DB
            db.commit()

    def get_top_entries(self):
        #gets top 5 records from table                                                         
            with sqlite3.connect(self.path) as db:                      #connects DB
                cursor = db.cursor()
                cursor.execute("SELECT * FROM Leaderboard ORDER BY Score DESC LIMIT 5") #top 5 scores
                entry = cursor.fetchall()
                return entry

    def get_player_entry(self):
         #get the most recently added score (players score)
            with sqlite3.connect(self.path) as db:                      #connects DB
                cursor = db.cursor()
                cursor.execute("SELECT * FROM Leaderboard ORDER BY ROWID DESC LIMIT 1") #last row 
                entry = cursor.fetchone()
                cursor.execute("SELECT * FROM Leaderboard ORDER BY Score DESC") #fetches all
                all_data = cursor.fetchall()
                for i in range(0,len(all_data)):    #linear seach for what row fetched entry at
                     if entry == all_data[i]:
                        rank = i+1 
                return entry , rank
        




