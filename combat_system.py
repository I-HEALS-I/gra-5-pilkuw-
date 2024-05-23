  
from dog import Dog



class CombatSystem:
    @staticmethod
    
    
    def fight(player, enemy):
        
        dog = None
        print(f"Player fights {enemy.name}!")
        
        while player.health > 0 and enemy.health > 0:
            
            if not dog:
                dog_choice = input("Do you want to summon your loyal dog? (y/n): ")
                
                if dog_choice.lower() == 'y':
                    dog = Dog()
                    print("Your loyal dog joins the fight!")

            
            
            enemy.health -= player.damage
            
            if dog:
                player_attack_choice = input("Do you want your loyal dog to attack? (y/n): ")
                
                if player_attack_choice.lower() == 'y':
                    dog.attack()
                    enemy.health -= dog.damage
                
                else:
                    dog.defend()
                    player.health += 20  
            player.health -= enemy.damage

            
            
            print(f"{player.name} has {player.health} health left.")
            print(f"{enemy.name} has {enemy.health} health left.")

        
        
        if player.health <= 0:
            print("You were defeated!")
        
        else:
            print(f"{enemy.name} was defeated!")

