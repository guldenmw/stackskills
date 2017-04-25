import random
import re
from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item


# Create Dark Magic
fire = Spell("Fire", 25, 600, "dark")
thunder = Spell("Thunder", 25, 600, "dark")
blizzard = Spell("Blizzard", 25, 600, "dark")
meteor = Spell("Meteor", 40, 1200, "dark")
quake = Spell("Quake", 14, 140, "dark")

# Create Good Magic
cure = Spell("Cure", 25, 620, "light")
cura = Spell("Cura", 32, 1500, "light")
curaga = Spell("Curaga", 50, 6000, "light")


# Create Some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super-Potion", "potion", "Heals 1000 HP", 1000)
elixir = Item("Elixer", "elixir", "Fully restores HP/MP of one part member", 9999)
megaelixir = Item("MegaElixer", "elixir", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_magic = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, curaga]

player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixir, "quantity": 5},
                {"item": megaelixir, "quantity": 2},
                {"item": grenade, "quantity": 5}]

# Instantiate People
player1 = Person("Mw   :", 3260, 132, 300, 34, player_magic, player_items)
player2 = Person("Valos:", 4160, 188, 311, 34, player_magic, player_items)
player3 = Person("Robot:", 3089, 174, 288, 34, player_magic, player_items)

enemy1 = Person("Imp  : ", 1250, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Magus:", 18200, 701, 525, 25, enemy_spells, [])
enemy3 = Person("Imp  : ", 1250, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("===============================")
    # print("\n")
    print("\nNAME                       HP                                     MP")

    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("    Choose actions: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemy_name = re.sub("[ |:]", "", enemies[enemy].name)
            enemies[enemy].take_damage(dmg)

            print("\nYou attacked " + enemy_name + " for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print("\n" + enemy_name + " has fallen.")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "light":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP" + bcolors.ENDC)

            elif spell.type == "dark":
                enemy = player.choose_target(enemies)
                enemy_name = re.sub("[ |:]", "", enemies[enemy].name)
                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg),
                      "points of damage " + "to " + enemy_name + "." + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemy_name + " has fallen.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose Item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + player.name[:-1] + " has no",
                      player.items[item_choice]["item"].name + "'s left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)

            elif item.type == "elixir":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp

                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp

                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemy_name = re.sub("[ |:]", "", enemies[enemy].name)
                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop),
                      "points of damage " + "to " + enemy_name + "." + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemy_name + " has fallen.")
                    del enemies[enemy]

    # Check if battle is over
    defeated_enemies = [enemy.name for enemy in enemies if enemy.get_hp() == 0]
    defeated_players = [player.name for player in players if player.get_hp() == 0]

    # Check if Player won
    if len(defeated_enemies) == 3:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False

    # Check if Enemy won
    elif len(defeated_players) == 3:
        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
        running = False

    # Enemy attack phase
    for enemy in enemies:
        enemy_name = re.sub("[ |:]", "", enemy.name)
        enemy_choice = random.randrange(0, 2)
        target = random.randrange(0, len(players))
        target_name = re.sub("[ |:]", "", players[target].name)

        if enemy_choice == 0:

            enemy_dmg = enemies[0].generate_damage()
            players[target].take_damage(enemy_dmg)

            print("\n" + enemy_name + " attacks " + target_name + " for " + str(enemy_dmg) + ".\n")

        elif enemy_choice == 1:
            # Chose Spell
            spell, magic_damage = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "light":
                # Chose Light Spell
                enemy.heal(magic_damage)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals " + enemy_name + " for",
                      str(magic_damage), "HP." + bcolors.ENDC)

            elif spell.type == "dark":
                # Chose Dark Spell
                players[target].take_damage(magic_damage)

                print(bcolors.OKBLUE + "\n" + enemy_name + "'s " + spell.name + " deals", str(magic_damage),
                      "points of damage " + "to " + target_name + ".\n" + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(target_name + " has fallen.")
                    del players[target]

            # print("Enemy chose", spell.name, "damage is", str(magic_damage) + ".\n")
