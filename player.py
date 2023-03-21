
class PLAYER:
    #姓名 金钱 攻击力 生命值 等级 经验值
    def __init__(self, name, money, attack, hp, level, exp):
        """姓名 金钱 攻击力 生命值 等级 经验值"""
        self.name = name
        self.money = money
        self.attack = attack
        self.hp = hp
        self.max_hp = hp
        self.level = level
        self.exp = exp
        self.backpack = ['木剑']
    
    def add_money(self, money):
        self.money += money
    def add_attack(self, attack):
        self.attack += attack
    def add_hp(self, hp):
        self.hp += hp
    def add_max_hp(self, max_hp):
        self.max_hp += max_hp
    def add_level(self, level):
        self.level += level
    def add_exp(self, exp):
        self.exp += exp
    def add_all(self, money, attack, hp, level, exp):
        self.money += money
        self.attack += attack
        self.hp += hp
        self.level += level
        self.exp += exp
    def add_backpack(self, item):
        self.backpack.append(item)
    def del_item(self, item):
        self.backpack.remove(item)
    def __dict__(self):
        return {"name":self.name, "money":self.money, "attack":self.attack, "hp":self.hp, "max_hp":self.max_hp, "level":self.level, "exp":self.exp, "backpack":self.backpack}
