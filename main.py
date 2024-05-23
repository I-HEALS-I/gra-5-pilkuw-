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
        
        print(f"{self.name} attacks for {self.damage} damage!")

    
    
    def display_stats(self):
        
        print(f"Name: {self.name}")
        print(f"Health: {self.health}")
        print(f"Damage: {self.damage}")
        print(f"Armor: {self.armor}")
        
        if self.ability:
            print(f"Ability: {self.ability}")




class King(Character):
    
    
    def __init__(self):
        
        super().__init__("King", health=10, damage=5, armor=0, ability="Summons guards")




class Prophet(Character):
    
    
    def __init__(self):
        
        super().__init__("Prophet", health=100, damage=10, armor=0, ability="Foresees the next move in the maze")




class Mage(Character):
    
    
    def __init__(self):
        
        super().__init__("Mage", health=80, damage=150, armor=0)




class Knight(Character):
    
    
    def __init__(self):
        
        super().__init__("Knight", health=120, damage=25, armor=0)




class Goblin(Character):
    
    
    def __init__(self):
        
        super().__init__("Goblin", health=200, damage=25, armor=0)




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




def ustal_parametry_poziomu(wybur_postaci):
    
    if wybur_postaci == 1:
        return 10, 10
    
    elif wybur_postaci == 2:
        return 50, 50
    
    elif wybur_postaci == 3:
        return 100, 100




def wybierz_postac():
    
    print("Wybierz swojego bohatera:")
    print("1. Wróżbita (stary i słaby, ale może sprawdzać najkrótszą drogę do wyjścia)")
    print("2. Mag (może nie najzręczniejszy, ale bardzo potężny)")
    print("3. Król (sam nie da rady, ale jego straż królewska nie ma sobie równych)")
    print("4. Rycerz (standardowa postać uniwersalna i dobra w wszystkim)")
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




def generate_location():
    
    locations = [Forest(), Cave(), Swamp(), Mountain()]
    return random.choice(locations)




class NPC:
    
    
    def __init__(self, name):
        
        self.name = name
        self.fabula = "Cześć, jestem " + self.name + ". Opowiem ci trochę o tej okolicy..."

    
    
    def offer_quest(self):
       
        print("Witaj, potrzebuję twojej pomocy.")
        print("1. Pokonaj przeciwnika")
        print("2. Znajdź przedmiot")
        choice = input("Twój wybór (1-2): ")
        
        if choice == "1":
            return "fight_enemy"
        
        elif choice == "2":
            return "find_item"
        
        else:
            print("Niepoprawny wybór.")
            return None

    
    
    def reward_player(self, quest_type):
        
        if quest_type == "fight_enemy":
            print("Dzięki za pomoc! Oto twoja nagroda.")
            return random.randint(50, 100)
        
        elif quest_type == "find_item":
            print("Bardzo miło! Oto twoja nagroda.")
            return random.choice(["Mikstura lecząca", "Mikstura zwiększająca obrażenia"])
        
        else:
            return None




def interact_with_npc(player_gold, inventory):
    
    npc_name = random.choice(["Grzegorz", "Marian", "Jadwiga", "Zofia"])
    npc = NPC(npc_name)
    quest_type = npc.offer_quest()
    
    if quest_type:
        reward = npc.reward_player(quest_type)
        
        if reward:
            
            if isinstance(reward, int):
                player_gold += reward
                print(f"Zdobyłeś {reward} złota.")
           
            else:
                inventory.add_item(Item(reward, {"health": 0, "damage": 0, "armor": 0}))
                print(f"Zdobyłeś przedmiot: {reward}")
    return player_gold




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




def main():
    
    player_gold = 200
    ekwipunek = Inventory()  # Inicjalizacja ekwipunku

    
    
    poziom_trudnosci = wybierz_poziom_trudnosci()
    szerokosc, wysokosc = ustal_parametry_poziomu(poziom_trudnosci)

    
    
    print(f"Wybrany poziom trudności: {poziom_trudnosci}")
    print(f"Wymiary labiryntu: {szerokosc}x{wysokosc}")

    
    
    postac = stworz_postac(wybierz_postac())
    postac.display_stats()

   
   
    maze = generate_maze(szerokosc, wysokosc)
    print("Maze generated!")

    
    
    current_column = 0  # Początkowa kolumna, gdzie znajduje się gracz

    
    
    if szerokosc == 10:
        max_ruchy = 10
    
    
    elif szerokosc == 50:
        max_ruchy = 50
    
   
    elif szerokosc == 100:
        max_ruchy = 100
    
  
    else:
        max_ruchy = 10  # Domyślny limit dla innych rozmiarów labiryntu

    
    
    print(f"Maksymalna liczba ruchów: {max_ruchy}")

    liczba_skrętów = 0

    
    
    # Główna pętla gry
   
    for _ in range(max_ruchy):
        current_column, skręt = poruszanie_sie(maze, current_column)
      
        if skręt != 0:
            print("Spotkałeś wroga!")
            enemy = Goblin()  # Losowy wybór wroga, można go zmienić na inny w zależności od poziomu trudności
            CombatSystem.fight(postac, enemy)
            liczba_skrętów += 1
            gold_amount = random.randint(20, 50) if isinstance(postac, Goblin) else random.randint(50, 100)
            player_gold += gold_amount
            print(f"Zdobyłeś {gold_amount} złota.")

            
            
            # Generowanie nowej lokacji po napotkaniu wroga
            location = generate_location()
            location.explore()
          
            if isinstance(location, Forest):
                postac.damage *= 1.15  # Efekt lasu: +15% do ataku
            
          
            elif isinstance(location, Cave):
                postac.health *= 1.2  # Efekt jaskini: +20% do zdrowia
            
          
            elif isinstance(location, Swamp):
                postac.damage *= 1.1  # Efekt bagien: +10% do obrażeń
            
           
            elif isinstance(location, Mountain):
                postac.armor += 25  # Efekt gór: +25 do pancerza

            merchant = Merchant()
            print("W lesie pojawił się tajemniczy kupiec.")
            player_gold -= merchant.sell_goods(player_gold, ekwipunek)

           
           
            # Interakcja z NPC po walce
            player_gold = interact_with_npc(player_gold, ekwipunek)

           
           
            # Wybór używania przedmiotu przed walką
            print("Czy chcesz użyć przedmiotu przed walką?")
            print("0. Anuluj")
            ekwipunek.display_inventory()
            choice = input("Twój wybór: ")
          
            if choice == "0":
                print("Anulowano.")
            
          
            elif choice.isdigit() and 1 <= int(choice) <= len(ekwipunek.items):
                selected_item = ekwipunek.items[int(choice) - 1]
                selected_item.use(postac)
            
          
            else:
                print("Niepoprawny wybór.")

        
        
       
        if current_column == len(maze[0]) - 1:
            print("Gratulacje, dotarłeś do końca labiryntu!")
            break

        
        
        # Sprawdź czy gracz znajduje się w górach
       
        if isinstance(location, Mountain):
            print("Jesteś w górach! Gra się kończy.")
            break

        
        
        # Sprawdź czy gracz ma jeszcze punkty życia
       
        if postac.health <= 0:
            print("Twoja postać zginęła! Gra się kończy.")
            break

    
    
   
    else:
        print("Przekroczyłeś maksymalną liczbę ruchów. Gra się kończy.")

    print(f"Liczba wykonanych skrętów: {liczba_skrętów}")
    print(f"Twój aktualny stan złota: {player_gold}")




if __name__ == "__main__":
    main()
 
