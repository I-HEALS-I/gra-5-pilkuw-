from maze_generator import generate_maze
from enemies import *
from combat_system import CombatSystem
from dog import Dog
import random


class Location:
    def __init__(self, name, effect=None):
        self.name = name
        self.effect = effect

    def explore(self):
        print(f"Jesteś w {self.name}. Co chcesz zrobić?")
        if self.effect:
            print(f"Efekt: {self.effect}")


class Forest(Location):
    def __init__(self):
        super().__init__("Las", effect="+15% do ataku")


class Cave(Location):
    def __init__(self):
        super().__init__("Jaskinia", effect="+20% do zdrowia")


class Swamp(Location):
    def __init__(self):
        super().__init__("Bagna", effect="+10% do obrażeń")


class Mountain(Location):
    def __init__(self):
        super().__init__("Góry", effect="+25% do obrony")


class Character:
    def __init__(self, name, health, damage, armor=0, ability=None):
        self.name = name
        self.health = health
        self.damage = damage
        self.armor = armor
        self.ability = ability

    def attack(self):
        print(f"{self.name} atakuje za {self.damage} obrażeń!")

    def display_stats(self):
        print(f"Imię: {self.name}")
        print(f"Zdrowie: {self.health}")
        print(f"Obrażenia: {self.damage}")
        print(f"Pancerz: {self.armor}")
        if self.ability:
            print(f"Umiejętność: {self.ability}")


class King(Character):
    def __init__(self):
        super().__init__("Król", health=10, damage=5, armor=0, ability="Przywołuje strażników")


class Prophet(Character):
    def __init__(self):
        super().__init__("Prorok", health=100, damage=10, armor=0, ability="Przewiduje następny ruch w labiryncie")


class Mage(Character):
    def __init__(self):
        super().__init__("Mag", health=80, damage=150, armor=0)


class Knight(Character):
    def __init__(self):
        super().__init__("Rycerz", health=120, damage=25, armor=0)


class Goblin(Character):
    def __init__(self):
        super().__init__("Goblin", health=200, damage=25, armor=0)


class Boss(Character):
    def __init__(self):
        super().__init__("Boss", health=500, damage=50, armor=100)


class Merchant:
    def __init__(self):
        self.items_for_sale = [
            Item("Mikstura lecząca", {"health": 20}),
            Item("Mikstura zwiększająca obrażenia", {"damage": 30}),
            Item("Mikstura zwiększająca zdrowie", {"health": 40}),
            Item("Ochronna tarcza", {"armor": 50})
        ]
        self.gold_min = 20
        self.gold_max = 50

    def offer_goods(self):
        print("Kupiec oferuje Ci swoje towary:")
        for idx, item in enumerate(self.items_for_sale, 1):
            print(f"{idx}. {item.name} ({self.gold_min * idx} złota)")

    def sell_goods(self, player_gold, ekwipunek):
        self.offer_goods()
        while True:
            choice = input("Twój wybór (1-4) lub Enter aby zignorować ofertę: ")
            if choice == "":
                print("Decydujesz się zignorować ofertę kupca.")
                return 0
            elif choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= 4:
                    item_price = self.gold_min * choice
                    if player_gold >= item_price:
                        print(f"Kupujesz przedmiot {choice}.")
                        selected_item = self.items_for_sale[choice - 1]
                        ekwipunek.add_item(selected_item)
                        return item_price
                    else:
                        print("Nie masz wystarczająco złota.")
                else:
                    print("Proszę wybrać liczbę od 1 do 4.")
            else:
                print("Proszę podać liczbę.")


class Item:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

    def use(self, character):
        if 'health' in self.effect:
            character.health += self.effect['health']
            print(f"{character.name} użył {self.name}. Zdrowie zostało zwiększone o {self.effect['health']}.")
        elif 'damage' in self.effect:
            character.damage += self.effect['damage']
            print(f"{character.name} użył {self.name}. Obrażenia zostały zwiększone o {self.effect['damage']}.")
        elif 'armor' in self.effect:
            character.armor += self.effect['armor']
            print(f"{character.name} użył {self.name}. Pancerz został zwiększony o {self.effect['armor']}.")


class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def display_inventory(self):
        print("Twój ekwipunek:")
        for idx, item in enumerate(self.items, 1):
            print(f"{idx}. {item.name}")


def wybierz_poziom_trudnosci():
    print("Wybierz poziom trudności:")
    print("1. Łatwy")
    print("2. Średni")
    print("3. Trudny")
    while True:
        wybur_poziomu_input = input("Twój wybór (1-3): ")
        if wybur_poziomu_input.isdigit():
            wybur_poziomu = int(wybur_poziomu_input)
            if 1 <= wybur_poziomu <= 3:
                return wybur_poziomu
            else:
                print("Proszę wybrać liczbę od 1 do 3.")
        else:
            print("Proszę podać liczbę.")


def ustal_parametry_poziomu(wybur_poziomu):
    if wybur_poziomu == 1:
        return 10, 10
    elif wybur_poziomu == 2:
        return 50, 50
    elif wybur_poziomu == 3:
        return 100, 100


def wybierz_postac():
    print("Wybierz swojego bohatera:")
    print("1. Prorok (stary i słaby, ale może sprawdzać najkrótszą drogę do wyjścia)")
    print("2. Mag (może nie najzręczniejszy, ale bardzo potężny)")
    print("3. Król (sam nie da rady, ale jego straż królewska nie ma sobie równych)")
    print("4. Rycerz (standardowa postać uniwersalna i dobra we wszystkim)")
    print("5. Goblin (bonus do zarabiania i potężna ilość życia)")
    while True:
        wybor_postaci_input = input("Twój wybór (1-5): ")
        if wybor_postaci_input.isdigit():
            wybor_postaci = int(wybor_postaci_input)
            if 1 <= wybor_postaci <= 5:
                return wybor_postaci
            else:
                print("Proszę wybrać liczbę od 1 do 5.")
        else:
            print("Proszę podać liczbę.")


def stworz_postac(wybor_postaci):
    if wybor_postaci == 1:
        return Prophet()
    elif wybor_postaci == 2:
        return Mage()
    elif wybor_postaci == 3:
        return King()
    elif wybor_postaci == 4:
        return Knight()
    elif wybor_postaci == 5:
        return Goblin()


def poruszanie_sie(maze, current_column):
    print("Możliwe kierunki: ")
    print("1. Lewo")
    print("2. Prawo")
    while True:
        wybor_kierunku_input = input("Twój wybór (1-2): ")
        if wybor_kierunku_input.isdigit():
            wybor_kierunku = int(wybor_kierunku_input)
            if wybor_kierunku in [1, 2]:
                print("Idziesz w lewo." if wybor_kierunku == 1 else "Idziesz w prawo.")
                return current_column - 1 if wybor_kierunku == 1 else current_column + 1, wybor_kierunku
            else:
                print("Proszę wybrać 1 lub 2.")
        else:
            print("Proszę podać liczbę.")


def main():
    # Inicjalizacja systemu walki
    combat_system = CombatSystem()

    # Generowanie labiryntu
    maze = generate_maze()
    current_row, current_column = 0, 0

    # Wybór poziomu trudności
    wybur_poziomu = wybierz_poziom_trudnosci()
    player_gold, liczba_ruchow = ustal_parametry_poziomu(wybur_poziomu)

    # Wybór postaci
    wybor_postaci = wybierz_postac()
    player = stworz_postac(wybor_postaci)
    player.display_stats()

    # Inicjalizacja ekwipunku
    ekwipunek = Inventory()

    # Tworzenie bossa
    boss = Boss()

    while current_row != len(maze) - 1:
        current_column, wybor_kierunku = poruszanie_sie(maze, current_column)

        current_row += 1

        location = maze[current_row][current_column]
        location.explore()

        # Walka z wrogiem
        enemy = Enemy.create_random_enemy(wybur_poziomu)
        combat_system.fight(player, enemy)

        # Spotkanie kupca
        if random.choice([True, False]):
            merchant = Merchant()
            player_gold -= merchant.sell_goods(player_gold, ekwipunek)

        # Check if boss should appear
        if current_row == len(maze) - 2:
            print("Boss nadchodzi!")
            combat_system.fight(player, boss)

        # Użycie przedmiotu
        if random.choice([True, False]):
            if ekwipunek.items:
                item = random.choice(ekwipunek.items)
                item.use(player)

        # Wyświetlanie stanu bohatera
        player.display_stats()
        print(f"Złoto: {player_gold}")

    print("Gratulacje! Przeszedłeś przez labirynt.")


if __name__ == "__main__":
    main()
