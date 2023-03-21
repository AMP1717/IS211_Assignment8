import random
import argparse
import time

class Die:
    def __init__(self, use_random_seed=False):
        if use_random_seed:
            random.seed()
        else:
            random.seed(0)
    
    def roll(self, silent=False):
        if not silent:
            input("\nPress Enter to roll the die!")
        num = random.randrange(1, 7)
        if not silent:
            print(f"You rolled {num}!\n")
        return num


class Player:
    def __init__(self, player_number):
        self.num = player_number
        self.score = 0
    
    def play(self, target, die):
        pass
        #to be implemented in child classes

class HumanPlayer(Player):
    def __init__(self, player_number):
        super().__init__(player_number)

    def get_response(self):
        while True:
            response = input("Do you want to Roll or Hold (enter 'r' or 'h')? ").lower()
            if response in ["h", "hold"]:
                return "h"
            if response in ["r", "roll"]:
                return "r"
            print("Invalid input, try again.")
    
    def play(self, target, die):
        print(f"Player {self.num}, it is your turn, your score is {self.score}/{target}.")
        total = 0
        while True:
            roll = die.roll()

            if roll == 1:
                print(f"You rolled 1, your turn is over, your score is still {self.score}.")
                break

            total += roll
            if self.score + total >= target:
                self.score += total
                return
            
            print(f"This turn you got a total of {total}, which will increase your score from {self.score} to {self.score + total}")
            response = self.get_response()
            if response == 'h':
                self.score += total
                print(f"You added {total} to your score, your score is now {self.score}.")
                break

        input("Press Enter to end your turn.")

class ComputerPlayer(Player):
    def __init__(self, player_number):
        super().__init__(player_number)
    
    def play(self, target, die):
        print(f"Computer player {self.num}, it is your turn, your score is {self.score}/{target}.")
        total = 0
        while True:
            roll = die.roll(silent=True)

            if roll == 1:
                print(f"You rolled 1, your turn is over, your score is still {self.score}.")
                break

            total += roll
            if self.score + total >= target:
                self.score += total
                return
            
            if total > 25:
                self.score += total
                print(f"You added {total} to your score, your score is now {self.score}.")
                break

        input("Press Enter to end computer player turn.")

class PlayerFactory:
    def __init__(self):
        pass

    def create(self, number, playerType):
        if playerType == "human":
            return HumanPlayer(number)
        else:
            return ComputerPlayer(number)

class Game:
    def __init__(self, number_of_players=2, use_random_seed=False, target=100, player_types=None):
        if player_types == None:
            player_types = ["computer", "computer"]

        if number_of_players <= 1:
            raise ValueError("You need at least 2 players.")

        if len(player_types) < number_of_players:
            for _ in range(number_of_players - len(player_types)):
                player_types.append("computer")
        
        playerMaker = PlayerFactory()

        self.die = Die(use_random_seed)
        self.target = target
        self.players = []
        self.current_player_index = 0

        for i in range(number_of_players):
            playerType = player_types[i]
            self.players.append(playerMaker.create(i + 1, playerType))
        

    def _get_current_player(self):
        return self.players[self.current_player_index]

    def _get_current_score(self):
        return self.players[self.current_player_index].score

    def _check_player_win(self):
        if self._get_current_score() >= self.target:
            return True
        return False

    def _move_player_index(self):
        self.current_player_index += 1
        if self.current_player_index == len(self.players):
            self.current_player_index = 0

    def print_scores(self):
        print("\nCurrent scores:")
        for player in self.players:
            if isinstance(player, HumanPlayer):
                print(f"   Player {player.num}: {player.score}/{self.target}")
            else:
                print(f"AI Player {player.num}: {player.score}/{self.target}")

        print()
        print(f"Next player is player {self.current_player_index + 1}.")
        print()

    def play(self):
        print(f"Welcome to pig game, try to hit target score of {self.target} first!")
        print(f"Rolling 1 ends your turn, rolling 2 - 5 gives you option to roll again or hold.")
        self.print_scores()
        while True:
            self._get_current_player().play(self.target, self.die)
            if self._check_player_win():
                print()
                print(f"Congratulations player {self.current_player_index + 1}, you reached the target of {self.target} and you have won!")
                break
            self._move_player_index()
            self.print_scores()        
        
class TimedGameProxy(Game):
    def __init__(self, number_of_players=2, use_random_seed=False, target=100, player_types=None):
        super().__init__(number_of_players, use_random_seed, target, player_types)
        self.start = time.time()

    def check_timer(self):
        if time.time() - self.start <= 60:
            return False
        
        winner = max(self.players, key=lambda x: x.score)
        print("Timer ran out.")
        print(f"Congratulations player {winner.num}, you won with score {winner.score}!")
        return True


    def play(self):
        print(f"Welcome to pig game, try to hit target score of {self.target} first!")
        print(f"Rolling 1 ends your turn, rolling 2 - 5 gives you option to roll again or hold.")
        self.print_scores()
        while True:
            self._get_current_player().play(self.target, self.die)
            if self._check_player_win():
                print()
                print(f"Congratulations player {self.current_player_index + 1}, you reached the target of {self.target} and you have won!")
                break
            self._move_player_index()
            if self.check_timer():
                break
            self.print_scores()        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--player1", help="Player 1 type", type=str, required=True, choices=["human", "computer"])
    parser.add_argument("--player2", help="Player 2 type", type=str, required=True, choices=["human", "computer"])
    parser.add_argument("--timed", help="Enable 60 sec game limit", action='store_true')
    args = parser.parse_args()
    if args.timed:
        GameType = TimedGameProxy
    else:
        GameType = Game
    g = GameType(use_random_seed=True, 
             target=100, 
             number_of_players=2,
             player_types=[args.player1, args.player2])
    g.play()

main()