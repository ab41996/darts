import re
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Mount the directory containing index.html as a static directory
# app.mount("/", StaticFiles(directory="templates", html=True), name="static")

matches = {1:{}}

class Throw:
    def __init__(self, player_name, base_number, multiplier):
        self.player_name = player_name
        self.base_number = base_number
        self.multiplier = multiplier
        self.score = base_number * multiplier

        if self.score is not None:
            print(f"{self.player_name} scored {self.score}")

    @classmethod
    def from_input(cls, player_name, throw_input):
        letters = ''.join(re.findall(r'[a-zA-Z]', throw_input))
        numbers = int(''.join(re.findall(r'[0-9]', throw_input)))
        base_number = numbers
        multiplier = {"": 1, "d": 2, "t": 3, "D": 2, "T": 3}[letters]
        return cls(player_name, base_number, multiplier)


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


class Match():
    def __init__(self, player1_name, player2_name, type):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.type = type
        self.legs = []
        self.winner = ""

    def add_leg(self, leg):
        if leg.player1_name == self.player1_name:
            if leg.player2_name == self.player2_name:
                self.legs.append(leg)
            else:
                raise ValueError(f"Invalid player: {leg.player2_name}")
        else:
            raise ValueError(f"Invalid player: {leg.player1_name}")

@app.post("/throw/{player_name}")
def add_throw(player_name: str, throw_input: str):
    throw = Throw.from_input(player_name, throw_input)
    return {"message": f"{player_name} scored {throw.score}"}


@app.post("/visit/{player_name}")
def add_visit(player_name: str):
    visit = Visit(player_name)
    return {"message": f"{player_name} is up!!"}


@app.post("/leg/{player1_name}/{player2_name}")
def add_leg(player1_name: str, player2_name: str):
    leg = Leg(player1_name, player2_name)
    return {"message": f"{player1_name} vs {player2_name}!! Let's Gooo!!"}

@app.get('/test/{id}')
def test(id):
    return {"test_id": id}

@app.post("/match/{player1_name}/{player2_name}/{type}") #Operational
def start_match(player1_name: str, player2_name: str, type: int):
    match = Match(player1_name, player2_name, type)
    match_id = player1_name+player2_name+str(type)
    if match_id in matches:
        return {"Match already exists"}
    else:
        matches[match_id] = match
    return {"message": "{type} Match started {player1_name} vs {player2_name}!",
            "match": matches[match_id]}

@app.get("/get_match/{match_id}") #Operational
def get_match(match_id: str):
    return matches[match_id]
        

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