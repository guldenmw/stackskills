import random


class bcolors(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[94m'


class Person(object):
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]
        self.name = name

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print("\n    " + bcolors.BOLD + self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD + "    ACTIONS:" + bcolors.ENDC)
        for item in self.actions:
            print("        " + str(i) + ":", item)
            i += 1

    def choose_magic(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "    MAGIC:" + bcolors.ENDC)
        for spell in self.magic:
            print("        " + str(i) + ": " + spell.name, "(cost", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "    ITEMS: " + bcolors.ENDC)
        for item in self.items:
            print("        " + str(i) + ". " + item["item"].name + ":", item["item"].description,
                  " (x" + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        i = 1
        ii = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "    TARGET:" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("        " + str(i) + '.', enemy.name)
                i += 1

        choice = int(input("    Choose target: ")) - 1
        return choice

    def get_enemy_stats(self):
        hp_bar = ""
        bar_ticks = (self.hp / self.maxhp) * 100 / 2

        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        shp = ' '
        ahp = 6 - len(str(self.hp))
        chp = shp * ahp + str(self.hp)

        print(bcolors.BOLD + self.name + "        " +
              chp + "/" + str(self.maxhp) + "|" + bcolors.FAIL + hp_bar +
              bcolors.ENDC + bcolors.BOLD + "|     " + bcolors.ENDC)

    def get_stats(self):
        # print("                           _________________________            __________ ")
        hp_bar = ""
        hp_ticks = (self.hp/self.maxhp) * 100 / 4
        mp_bar = ""
        mp_ticks = (self.mp / self.maxmp) * 100 / 10

        while hp_ticks > 0:
            hp_bar += "█"
            hp_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        while mp_ticks > 0:
            mp_bar += "█"
            mp_ticks -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        shp = ' '
        ahp = 4 - len(str(self.hp))
        chp = shp * ahp + str(self.hp)

        smp = ' '
        amp = 4 - len(str(self.mp))
        cmp = smp * amp + str(self.mp)

        print(bcolors.BOLD + self.name + "           " +
              chp + "/" + str(self.maxhp) + "|" + bcolors.OKGREEN + hp_bar +
              bcolors.ENDC + bcolors.BOLD + "|     " +
              cmp + "/" + str(self.maxmp) + "|" + bcolors.OKBLUE + mp_bar + bcolors.ENDC +
              bcolors.BOLD + "|" + bcolors.ENDC)

    def choose_enemy_spell(self):
        if self.mp == 0:

        magic_choice = random.randrange(0, len(self.magic))

        spell = self.magic[magic_choice]
        magic_damage = spell.generate_damage()

        if spell.cost > self.get_mp():
            self.choose_enemy_spell()
        else:
            return spell, magic_damage
