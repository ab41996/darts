import re
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, validator
import sqlite3

app = FastAPI()

# # Mount the directory containing index.html as a static directory
# app.mount("/static", StaticFiles(directory="templates", html=True), name="static")

# Connect to SQLite database
conn = sqlite3.connect('darts.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS matches
             (id INTEGER PRIMARY KEY, player1_name TEXT, player2_name TEXT, match_type INTEGER)''')

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS throws
             (id INTEGER PRIMARY KEY, match_id INTEGER, player_name TEXT, base_number INTEGER, multiplier TEXT, score INTEGER)''')

matches = {1:{}}


class Throw(BaseModel):
    player_name: str
    throw_input: str
    
    # base_number: int = Field(..., ge=1)
    # multiplier: str = Field(..., pattern="^[sdt]$")  # Accepts "s", "d", or "t"
    # score: int = Field(..., ge=0)

    # @validator("base_number", pre=True)
    # def extract_base_number(cls, v, values):
    #     throw_input = values.get("throw_input")
    #     try:
    #         base_number = int(throw_input[1:])  # Extract digits after "d"
    #     except ValueError:
    #         raise ValueError("Invalid throw input format")
    #     return base_number

    # @validator("multiplier", pre=True)
    # def extract_multiplier(cls, v, values):
    #     throw_input = values.get("throw_input")
    #     if throw_input[0] not in ("s", "d", "t"):
    #         raise ValueError("Invalid throw input format")
    #     return throw_input[0]

    # @validator("score", pre=True)
    # def calculate_score(cls, v, values):
    #     multiplier = values.get("multiplier")
    #     base_number = values.get("base_number")
    #     if multiplier == "d":
    #         return base_number * 2
    #     elif multiplier == "t":
    #         return base_number * 3
    #     else:
    #         return base_number


class Visit:
    def __init__(self, player_name):
        self.player_name = player_name
        self.throws = []
        print(f"{player_name} is up!!")

    def add_throw(self, throw):
        if len(self.throws) >= 3:
            print("Max throws reached")
        else:
            self.throws.append(throw)


class Leg:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_visits = []
        self.player2_visits = []
        self.player1_score = 0
        self.player2_score = 0
        self.winner = ""
        print(f"{self.player1_name} vs {self.player2_name}!! Let's Gooo!!")

    def add_visit(self, visit):
        if visit.player_name == self.player1_name:
            self.player1_visits.append(visit)
            self.score_update()
        elif visit.player_name == self.player2_name:
            self.player2_visits.append(visit)
            self.score_update()
        else:
            raise ValueError(f"Invalid player: {visit.player_name}")

    def score_update(self):
        self.player1_score = sum(throw.score for visit in self.player1_visits for throw in visit.throws)
        self.player2_score = sum(throw.score for visit in self.player2_visits for throw in visit.throws)
        print(f"Scores on the doors.. {self.player1_name}: {self.player1_score}, {self.player2_name}: {self.player2_score}")


class Match(BaseModel):
    player1_name: str
    player2_name: str
    match_type: int


@app.post("/throw/{player_name}")
def add_throw(player_name: str, throw_input: str):
    throw = Throw.from_input(player_name, throw_input)
    return {"message": f"{player_name} scored {throw.score}"}

@app.post("/match/")
async def start_match(match: Match):
    c.execute("INSERT INTO matches (player1_name, player2_name, match_type) VALUES (?, ?, ?)",
              (match.player1_name, match.player2_name, match.match_type))
    conn.commit()
    match_id = c.lastrowid
    return {
        "message": f"Match {match_id} started {match.player1_name} vs {match.player2_name}!",
        "match_id": match_id,
        "player1_name": match.player1_name,
        "player2_name": match.player2_name,
    }

@app.post("/match/{match_id}/throws")
async def submit_throw(match_id: int, throw: Throw):
    # Extract values from the throw input
    try:
        multiplier = throw.throw_input[0]
        base_number = int(throw.throw_input[1:])
    except (IndexError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid throw input format")
    
    # Calculate the score based on the multiplier
    if multiplier == 'd':
        score = base_number * 2
    elif multiplier == 't':
        score = base_number * 3
    elif type(multiplier) == int:
        base_number = throw.throw_input * 1
        score = base_number
        multiplier = "s"
    else:
        raise HTTPException(status_code=400, detail="Invalid multiplier")
    
    # Insert the throw data into the database
    c.execute("INSERT INTO throws (match_id, player_name, base_number, multiplier, score) VALUES (?, ?, ?, ?, ?)",
              (match_id, throw.player_name, base_number, multiplier, score))
    conn.commit()
    
    # Get the ID of the last inserted row
    throw_id = c.lastrowid
    
    # Return a success message
    return {
        "message": f"Throw {throw_id} submitted by {throw.player_name} scored {score}!",
        "match_id": match_id
    }

@app.post("/hello")
def hello():
    return {"message": "Hello World"}

# Interactive section below!!

# player1_name = input("Enter name for Player 1: ")
# player2_name = input("Enter name for Player 2: ")

# leg1 = Leg(player1_name, player2_name)

# for _ in range(3):  # Assume each visit consists of 3 throws
#     visit = Visit(player1_name)
#     for _ in range(3):
#         throw = Throw.from_input(player1_name)
#         visit.add_throw(throw)
#     leg1.add_visit(visit)

#     visit = Visit(player2_name)
#     for _ in range(3):
#         throw = Throw.from_input(player2_name)
#         visit.add_throw(throw)
#     leg1.add_visit(visit)
