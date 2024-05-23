class Enemy:
    
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage

    def attack(self):
        print(f"{self.name} attacks for {self.damage} damage!")



class King(Enemy):
    
    def __init__(self):
        super().__init__("King", health=10, damage=5)



class Prophet(Enemy):
    
    def __init__(self):
        super().__init__("Prophet", health=50, damage=10)



class Mage(Enemy):
    
    def __init__(self):
        super().__init__("Mage", health=40, damage=150)



class Knight(Enemy):
    
    def __init__(self):
        super().__init__("Knight", health=60, damage=25)



class Goblin(Enemy):
    
    def __init__(self):
        super().__init__("Goblin", health=100, damage=25)
