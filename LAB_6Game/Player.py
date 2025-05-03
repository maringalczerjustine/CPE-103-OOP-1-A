import random

# Base Player class
class Player:
    def __init__(self, name, health=100):
        self._name = name
        self._health = health
        self._wins = 0

    def get_health(self):
        return self._health

    def is_alive(self):
        return self._health > 0

    def take_damage(self, damage):
        self._health -= damage
        if self._health < 0:
            self._health = 0

    def attack(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def win(self):
        self._wins += 1

    def get_wins(self):
        return self._wins

    def reset_health(self):
        self._health = 100


class Swordsman(Player):
    def attack(self):
        damage = random.randint(10, 20)
        print(f"{self._name} attacks with sword for {damage} damage!")
        return damage

class Archer(Player):
    def attack(self):
        damage = random.randint(5, 25)
        print(f"{self._name} shoots an arrow for {damage} damage!")
        return damage

class Magician(Player):
    def attack(self):
        damage = random.randint(15, 30)
        print(f"{self._name} casts a spell for {damage} damage!")
        return damage

class Monster(Player):
    def attack(self):
        damage = random.randint(10, 15)
        print(f"{self._name} attacks ferociously for {damage} damage!")
        return damage