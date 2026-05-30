class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage


class HealingWeapon(Weapon):
    def __init__(self, name, damage, heal_power):
        super().__init__(name, damage)
        self.heal_power = heal_power


class Hero:
    def __init__(self, name, hp, weapon):
        self.name = name
        self.hp = hp
        self.weapon = weapon

    def heal(self, other):
        if hasattr(self.weapon, 'heal_power'):
                heal_amount = self.weapon.heal_power
                other.hp += heal_amount

                print(f"{self.name} HEALS {other.name} {heal_amount}")
                print(f"NOW, HP {other.name}: {other.hp}\n")

    def introduce(self):
        print(f"HERO: {self.name}")
        print(f"HP: {self.hp}")
        print(f"WEAPON: {self.weapon.name}\n")

    def attack(self, other):
        print(f"{self.name} ATTACKS {other.name} WITH A WEAPON {self.weapon.name}")
        other.hp -= self.weapon.damage

        print(f"{other.name} TAKES {self.weapon.damage} DAMAGE!")
        print(f"HP {other.name}: {other.hp}\n")


# WEAPONS

sword = Weapon("Sword", 15)
axe = Weapon("Axe", 20)
staff = HealingWeapon("Staff", 10, 30)

# HEROES

hero1 = Hero("Sock", 100, sword)
hero2 = Hero("Ceramic", 120, axe)
healer1 = Hero("SmartGuy", 80, staff) # A wise guy. He loves parkour.


# INFO

print("HEROES, INTRODUCE YOURSELF\n")

hero1.introduce()
hero2.introduce()
healer1.introduce()

# FIGHT

print("LET THE BATTLE BEGIN!\n")

hero1.attack(hero2)
hero2.attack(hero1)
healer1.heal(hero1)
hero1.attack(hero2)
hero2.attack(hero1)

# RESULTS

print("RESULTS:\n")

hero1.introduce()
hero2.introduce()
healer1.introduce()

