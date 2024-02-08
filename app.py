from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse  # Correct import for FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3
from datetime import datetime as dt

app = FastAPI()

# Serve static files (like JavaScript and CSS) from the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve HTML file from the 'templates' directory
@app.get("/", response_class=HTMLResponse)
def read_root():
    return FileResponse("templates/index.html")

# Create a SQLite database
conn = sqlite3.connect('darts.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS throws (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT,
        score INTEGER,
        multiplier INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()


class Throw:
    def __init__(self, player_name, score):
        self.player_name = player_name
        self.score = score
        self.timestamp = dt.now()

class Visit:
    def __init__(self, player_name):
        self.player_name = player_name
        self.throws = []

    def add_throw(self, score):
        self.throws.append(Throw(player_name=self.player_name, score=score))

class Leg:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.visits_player1 = []
        self.visits_player2 = []

    def add_visit(self, visit):
        if visit.player_name == self.player1:
            self.visits_player1.append(visit)
        elif visit.player_name == self.player2:
            self.visits_player2.append(visit)
        else:
            raise ValueError(f"Invalid player: {visit.player_name}")

class Match:
    def __init__(self):
        self.legs = []

    def add_leg(self, leg):
        self.legs.append(leg)

# Example usage:
match = Match()

# Add a leg with two players
leg1 = Leg(player1="Player1", player2="Player2")
match.add_leg(leg1)

# Add visits to the leg for each player
visit1_player1 = Visit(player_name="Player1")
visit1_player1.add_throw(score=20)
visit1_player1.add_throw(score=15)
leg1.add_visit(visit1_player1)

visit1_player2 = Visit(player_name="Player2")
visit1_player2.add_throw(score=10)
visit1_player2.add_throw(score=16)
leg1.add_visit(visit1_player2)

# Add another leg
leg2 = Leg(player1="Player1", player2="Player2")
match.add_leg(leg2)

# Add visits to the second leg for each player
visit2_player1 = Visit(player_name="Player1")
visit2_player1.add_throw(score=18)
visit2_player1.add_throw(score=13)
leg2.add_visit(visit2_player1)

visit2_player2 = Visit(player_name="Player2")
visit2_player2.add_throw(score=12)
visit2_player2.add_throw(score=17)
leg2.add_visit(visit2_player2)



@app.get("/")
def read_root():
    return {"message": "Darts App - FastAPI"}


@app.post("/record_throw")
def record_throw(throw: Throw):
    # Extract data from the request
    player_name = throw.playerName
    score = throw.score

    # Insert the throw into the database
    conn = sqlite3.connect('darts.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO throws (player_name, score) VALUES (?, ?)', (player_name, score))
    conn.commit()
    conn.close()

    return {"status": "success"}
