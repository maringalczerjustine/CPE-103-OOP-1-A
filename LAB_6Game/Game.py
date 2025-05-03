import random
from Player import Swordsman, Archer, Magician, Monster


class Game:
    def __init__(self):
        self.player1 = None
        self.player2 = None

    def select_role(self, name):
        role = input(f"{name}, select a role (Swordsman/Archer/Magician): ").strip().lower()
        if role == "swordsman":
            return Swordsman(name)
        elif role == "archer":
            return Archer(name)
        elif role == "magician":
            return Magician(name)
        else:
            print("Invalid choice. Defaulting to Swordsman.")
            return Swordsman(name)

    def single_player(self):
        name = input("Enter your name: ").strip()
        player = Swordsman(name)
        monster = Monster("Monster")

        wins_needed = 2
        while player.get_wins() < wins_needed:
            print(f"\n--- Match {player.get_wins() + 1}: {player._name} (Swordsman) vs Monster (Boss) ---\n")

            player.reset_health()
            monster.reset_health()

            self.play_match(player, monster)

            if player.is_alive():
                player.win()
                print(f"{name} wins this round! Total wins: {player.get_wins()}")
            else:
                print(f"{name} was defeated! Try again.")
                player.reset_health()
                monster.reset_health()  # Restart the current match if player is defeated

            if player.get_wins() == wins_needed:
                break

        print(f"\n{name} has won 2 matches! You can now select a new role.")
        # Preserve wins and update role
        new_role = self.select_role(name)
        player.__class__ = new_role.__class__  # Change the player's class to the new role
        player.reset_health()  # Reset health for the new role

        # Continue to play with the new role against the Monster
        match_number = 3  # Start from match 3
        while True:
            print(f"\n--- Match {match_number}: {player._name} ({type(player).__name__}) vs Monster (Boss) ---\n")
            player.reset_health()
            monster.reset_health()
            self.play_match(player, monster)

            if player.is_alive():
                player.win()  # Increment wins after winning a match with the new role
                print(f"{name} wins this round! Total wins: {player.get_wins()}")
            else:
                print(f"{name} was defeated! Try again.")
                player.reset_health()
                monster.reset_health()  # Restart the current match if player is defeated

            match_number += 1

            # Option to quit after each match
            quit_game = input("Do you want to quit? (yes/no): ").strip().lower()
            if quit_game == "yes":
                print("Thanks for playing!")
                break

        # Display total wins for the player
        print(f"\n{player._name}'s total wins: {player.get_wins()}")

    def player_vs_player(self):
        name1 = input("Enter name for Player 1: ").strip()
        name2 = input("Enter name for Player 2: ").strip()

        player1 = self.select_role(name1)
        player2 = self.select_role(name2)

        while player1.is_alive() and player2.is_alive():
            self.play_match(player1, player2)

            # Track wins for Player 1 and Player 2
            if not player2.is_alive():
                player1.win()
                print(f"{player1._name} wins this round! Total wins: {player1.get_wins()}")
            elif not player1.is_alive():
                player2.win()
                print(f"{player2._name} wins this round! Total wins: {player2.get_wins()}")

            # Reset health for the next match
            player1.reset_health()
            player2.reset_health()

            # Option to quit after each match
            quit_game = input("Do you want to quit? (yes/no): ").strip().lower()
            if quit_game == "yes":
                print("Thanks for playing!")
                break

        # Display total wins for both players
        print(f"\n{player1._name}'s total wins: {player1.get_wins()}")
        print(f"{player2._name}'s total wins: {player2.get_wins()}")

    def play_match(self, player1, player2):
        players = [player1, player2]
        random.shuffle(players)
        while player1.is_alive() and player2.is_alive():
            for player in players:
                if player.is_alive():
                    opponent = player2 if player == player1 else player1
                    damage = player.attack()
                    opponent.take_damage(damage)
                    print(f"{opponent._name} has {opponent.get_health()} health remaining.")
                    if not opponent.is_alive():
                        print(f"{opponent._name} has been defeated!")
                        break

    def start(self):
        mode = input("Select mode (Single Player/Player vs Player): ").strip().lower()
        if mode == "single player":
            self.single_player()
        elif mode == "player vs player":
            self.player_vs_player()
        else:
            print("Invalid mode. Exiting game.")