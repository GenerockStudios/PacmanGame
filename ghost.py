from player import Player 

# Classe des fantomes
class Ghost(Player):
    # cette fonction permet de changer la vitesse dún fantome
    def changespeed(self, list, ghost, turn, steps, l):
        try:
            z = list[turn][2]
            if steps < z:
                self.change_x = list[turn][0]  
                self.change_y = list[turn][1] 
                steps += 1
            else:
                if turn < l:
                    turn += 1
                elif ghost == "clyde":
                    turn = 2
                else:
                    turn = 0 
                self.change_x = list[turn][0] 
                self.change_y = list[turn][1] 
                steps = 0
            return [turn, steps] 
        except IndexError:  
            return [0,0]
        