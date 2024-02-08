#%%
class Throw:
    def __init__(self, player_name, base_number, multiplier):
        self.player_name = player_name
        self.base_number = base_number
        self.multiplier = multiplier
        self.score = base_number*multiplier

        print(f"{self.player_name} scored {self.score}")


throw1 = Throw(player_name="hayes", base_number=20, multiplier=3)
#%%
throw1.score
# %%
class Visit:
    def __init__(self, player_name):
        self.player_name = player_name
        self.throws = []
        print(f"{player_name} is up!!")

    def add_throw(self, base_number, multiplier):
        if len(self.throws) >= 3:
            print("Max throws reached")
        else:
            self.throws.append(Throw(player_name=self.player_name, base_number=base_number, multiplier=multiplier))
#%%

visit1 = Visit("hayes")
visit1.add_throw(20, 3)
visit1.add_throw(20, 3)
visit1.add_throw(20, 3)
visit1.add_throw(20, 3)

# %%

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
        self.player1_score = 0
        self.player2_score = 0

        for visit in self.player1_visits:
            for throw in visit.throws:
                self.player1_score += throw.score

        for visit in self.player2_visits:
            for throw in visit.throws:
                self.player2_score += throw.score
        print(f"Scores on the doors.. {self.player1_name}: {self.player1_score}, {self.player2_name}: {self.player2_score}")
            

#%%
leg1 = Leg("hayes", "anand")

visit2 = Visit("hayes")
visit2.add_throw(20, 3)
visit2.add_throw(20, 3)
visit2.add_throw(20, 3)
visit2.add_throw(20, 3)

leg1.add_visit(visit2)

visit3 = Visit("anand")
visit3.add_throw(10, 1)
visit3.add_throw(5, 1)
visit3.add_throw(12, 1)
visit3.add_throw(1, 1)

leg1.add_visit(visit3)

visit4 = Visit("max")
visit4.add_throw(10, 1)
visit4.add_throw(5, 1)
visit4.add_throw(12, 1)

leg1.add_visit(visit4)


# %%
class Match:
    def __init__(self, player1_name, player2_name, type):
        self.player1_name = player1_name
        self.player2_name = player2_name
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

#%%


        
