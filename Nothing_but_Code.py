import random  # FOR BATTLES AND CRIT.


class Weapon:
    """STORES WEAPON CHARACTERISTICS"""
    def __init__(self, name, damage):
        self.name = name  # WEAPON NAME (e.g. "SWORD")
        self.damage = damage  # DAMAGE VALUE (e.g. 15)


class HealingWeapon(Weapon):
    """HEALING WEAPON. LIKE NORMAL WEAPON BUT WITH HEALING POWER"""
    def __init__(self, name, damage, heal_power):
        super().__init__(name, damage)
        self.heal_power = heal_power  # e.g. +30 HP


class Hero:
    """HEROES"""
    def __init__(self, name, hp, weapon):
        """INITIALIZES HEROES"""
        self.name = name  # HERO NAME
        self.hp = hp  # HERO HEALTH (100, 120, etc.)
        self.weapon = weapon  # HERO WEAPON (OBJECT OF CLASS Weapon)

    def introduce(self):
        """PRINTS HERO INFORMATION, USE THIS FOR TEST"""
        print(f"HERO: {self.name}")
        print(f"HP: {self.hp}")
        print(f"WEAPON: {self.weapon.name}\n")

    def brief_intro(self, number):
        """SHORT HERO INFO FOR SELECTION MENU (LIKE introduce, BUT COOLER)"""
        print(f"{number}) {self.name} - HP: {self.hp}, {self.weapon.name} (dmg: {self.weapon.damage})")
        # FOR HEALING WEAPONS
        if hasattr(self.weapon, 'heal_power'):
            print(f"   (and heals {self.weapon.heal_power})")

    def attack(self, other):
        """SIMPLE: HERO ATTACKS HERO(ENEMY)"""
        print(f"{self.name} ATTACKS {other.name} WITH {self.weapon.name}")
        other.hp -= self.weapon.damage
        print(f"{other.name} TAKES {self.weapon.damage} DAMAGE!")
        print(f"{other.name}'s HP: {other.hp}\n")

    def heal(self, other):
        """HEAL ALLY (ONLY IF WEAPON CAN HEAL p.s. I avoid it)"""
        if hasattr(self.weapon, 'heal_power'):
            heal_amount = self.weapon.heal_power
            other.hp += heal_amount
            print(f"{self.name} HEALS {other.name} FOR {heal_amount} HP")
            print(f"{other.name}'s HP: {other.hp}\n")
        else:
            print(f"{self.name} CANNOT HEAL WITH {self.weapon.name}!\n") # JUST IN CASE :)


# FUNCTIONS


def show_status(player, ally, enemies):
    """DISPLAY CURRENT STATUS OF ALL CHARACTERS (I DON'T KNOW FOR WHAT, BECAUSE YOU ALREADY SEE IT)"""
    print(f"\n{player.name}: {player.hp} HP")
    print(f"{ally.name}: {ally.hp} HP")
    for e in enemies:
        print(f"{e.name}: {e.hp} HP")


def attack_action(attacker, enemies):
    """CHOOSE TARGET AND ATTACK!!"""
    while True:
        print("CHOOSE TARGET:")
        for i, e in enumerate(enemies, 1):
            print(f"{i}) {e.name}")
        try:
            index = int(input("> ")) - 1
            if 0 <= index < len(enemies):
                attacker.attack(enemies[index])
                if enemies[index].hp <= 0:
                    print(f"{enemies[index].name} DIES!")
                    enemies.pop(index)
                return True
            else:
                print(f"INVALID TARGET! ENTER NUMBER BETWEEN 1-{len(enemies)}")
        except ValueError:
            print("PLEASE ENTER A VALID NUMBER, GOD DAMN IT!")


def heal_action(healer, ally):
    """HANDLE HEAL ACTION - CHOOSE TARGET AND HEAL"""
    while True:
        print("1) SELF  2) ALLY")
        choice = input("> ")

        if choice == "1":
            healer.heal(healer)
            return True
        elif choice == "2":
            healer.heal(ally)
            return True
        else:
            print("INVALID CHOICE! ENTER 1 OR 2")


def choose_hero(hero_list):
    """SHOWS HERO LIST AND RETURNS SELECTED HERO"""
    print("\n" + "<>" * 8)
    print("CHOOSE YOUR HERO")
    print("<>" * 8)

    for i, hero in enumerate(hero_list, start=1):
        hero.brief_intro(i)

    while True:
        try:
            choice = int(input(f"ENTER NUMBER (1 - {len(hero_list)}): "))
            if 1 <= choice <= len(hero_list):
                return hero_list[choice - 1]
            else:
                print(f"WAIT, UNTIL I ADD MORE HEROES (PLEASE ENTER NUMBER BEETWEEN 1 AND {len(hero_list)}!)")
        except ValueError:
            print("NO, NO, NO, JUST NUMBER, OKAY?")


def setup_teams(hero_list, player_hero):
    """ASSIGNS ALLY AND ENEMIES AFTER PLAYER SELECTION"""
    remaining = [hero for hero in hero_list if hero != player_hero]
    ally = random.choice(remaining)
    enemies = [hero for hero in remaining if hero != ally]
    return ally, enemies


def battle(player, ally, enemies):
    """BATTLE SYSTEM"""
    print("\n" + "<>" * 20)
    print("BATTLE START!")
    print("<>" * 20)

    while player.hp > 0 and enemies:
        # PLAYER TURN
        print(f"\n{player.name} [HP: {player.hp}] | ALLY: {ally.name} [HP: {ally.hp}]")
        for i, e in enumerate(enemies, 1):
            print(f"ENEMY {i}: {e.name} [HP: {e.hp}]")

        # SHOW MENU BASED ON WEAPON TYPE
        if hasattr(player.weapon, 'heal_power'):
            print("\n1) ATTACK  2) HEAL  3) STATUS")
            choice = input("> ")
            if choice == "1":
                attack_action(player, enemies)
            elif choice == "2":
                heal_action(player, ally)
            elif choice == "3":
                show_status(player, ally, enemies)
                continue
            else:
                print("INVALID CHOICE!")
                continue
        else:
            print("\n1) ATTACK  2) STATUS")
            choice = input("> ")
            if choice == "1":
                attack_action(player, enemies)
            elif choice == "2":
                show_status(player, ally, enemies)
                continue
            else:
                print("INVALID CHOICE!")
                continue

        # CHECK VICTORY
        if not enemies:
            print("\nVICTORY! ALL ENEMIES ARE DEFEATED!")
            return True

        # CHECK IF YOU DIED
        if player.hp <= 0:
            print(f"\n{player.name} HAS FALLEN... YOU LOSE!")
            return False

        # ALLY TURN (ALL RANDOM)
        if ally.hp > 0 and enemies:
            print(f"\n{ally.name}'S TURN (ALLY):")
            ally.attack(enemies[0])
            if enemies[0].hp <= 0:
                print(f"{enemies[0].name} DIES!")
                enemies.pop(0)

        # ENEMIES TURN (RANDOM AGAIN)
        for enemy in enemies[:]:
            if enemy.hp > 0:
                print(f"\n{enemy.name}'S TURN (ENEMY):")
                target = player if random.choice([True, False]) else ally
                enemy.attack(target)
                if player.hp <= 0:
                    print(f"\n{player.name} HAS FALLEN... YOU LOSE!")
                    return False
        input("\n[PRESS ENTER TO CONTINUE]")
    if player.hp <= 0:
        print("\nYOU LOSE!")
        return False
    else:
        print("\nYOU WIN!")
        return True





# CREATE WEAPONS (FOR NOW THE WEAPON HAS BEEN APPROVED TO THE HERO)


sword = Weapon("SWORD", 15)
axe = Weapon("AXE", 20)
staff = HealingWeapon("STAFF", 10, 30)
knife = Weapon("KNIFE", 8)


# CREATE HEROES


all_heroes = [
    Hero("SOCK", 100, sword),
    Hero("CERAMIC", 120, axe),
    Hero("SMART_GUY", 80, staff),
    Hero("SHADOW", 90, knife),
]



# GAME START


# HERO SELECTION
player = choose_hero(all_heroes)


# TEAM ASSIGNMENT
ally, enemies = setup_teams(all_heroes, player)


# SHOW TEAMS
print("\n" + "<>" * 10)
print("TEAMS ARE SET!")
print("<>" * 10)
print(f"YOU: {player.name} (HP: {player.hp}, {player.weapon.name})")
print(f"ALLY: {ally.name} (HP: {ally.hp}, {ally.weapon.name})")
print(f"ENEMIES: {enemies[0].name} (HP: {enemies[0].hp}), {enemies[1].name} (HP: {enemies[1].hp})")

# BATTLE BEGINS
battle(player, ally, enemies)