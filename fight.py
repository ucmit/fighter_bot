from logging import FileHandler
import random
from time import sleep
import discord
from discord.ext import commands
import asyncio, os

from discord.member import Member

# f1_data = {
#     "member": {
#         "id": 9849681651,
#         "name": "Kenshi",
#         "msg" : discord.Message
#     },

#     "specs": {
#         "lvl": f1_lvl,
#         "hp": 100 + f1_lvl*10,
#         "exp": 0,
#         "crt": 10 + f1_lvl*5,
#         "dmg": int(20 + f1_lvl*1.2),
#     },
# }

attack_quets = {
    "attack" : [
        "рубит", 
        "бьёт по дых",
        "колит в глаз", 
        "забирает хавчик",
        "спел Моргенштерна"
    ],
    "finish" : [
        "вырвал хребет", 
        "сбил машиной",
        "повел на концерт Моргенштерна"
    ]
}

class Fighter():
    def __init__(self, member:dict, specs:dict):
        self._member = member
        self._specs = specs
        self._new_specs = specs
        self.can_fight = True

    async def attack(self, target:"Fighter"=None):
        # Реализация боя на основе тз
        attack_chance = random.randint(0, self._specs["dmg"])
        crit_chance = random.randint(1, 100)

        new_embed = discord.Embed(
            title = "Let's Mortal Kombat Begins!",
            description = f"{self._member['name']} {attack_quets['attack'][random.randint( 0, len(attack_quets['attack']) - 1 )]} {target._member['name']} ",
            colour = discord.Colour.dark_purple(),
        )
        
        if attack_chance > 0:
            new_embed.description += "и наносит "
            if crit_chance > 20:
                target._specs["hp"] -= self._specs["dmg"]
                new_embed.description += f'{self._specs["dmg"]} урона'
            else: 
                target._specs["hp"] -=  self._specs["dmg"] + self._specs["crt"]
                new_embed.description += f'{self._specs["dmg"] + self._specs["crt"]} урона'
        else:
            new_embed.description += "и промахивается"
        
        await self._member["msg"].edit(embed = new_embed)
    
        if target._specs["hp"] <= 0: 
            await asyncio.sleep(2)
            new_embed.description = f"{self._member['name']} {attack_quets['finish'][random.randint( 0, len(attack_quets['finish']) - 1 )]} {target._member['name']}! "
            await self._member["msg"].edit(embed = new_embed)
            target.can_fight = False

    async def win(self, target:"Fighter"=None):
        diff = abs(self._specs["lvl"] - target._specs["lvl"])
        
        # разница от 0 до 4
        if diff < 4:
            self._specs["exp"] += 10
        # разница от 4 до 9
        elif diff < 9:
            # если наш лвл больше противника
            if self._specs["lvl"] > target._specs["lvl"]:
                self._specs["exp"] -= 5
            # противниник выше лвл
            else:
                self._specs["exp"] += 20
        # разница больше 9
        elif diff >= 9:
            # если наш лвл больше противника
            if self._specs["lvl"] > target._specs["lvl"]:
                self._specs["exp"] -= 40
            # противниник выше лвл
            else:
                self._specs["exp"] += 80
            
        if self._specs["exp"] >= 100:
            self.__lvl_up()
        
        new_embed = discord.Embed(
            title = "Flawless Victory!",
            description = f"{self._member['name']} победил {target._member['name']} и выжил при {self._specs['hp']} hp",
            colour = discord.Colour.dark_purple(),
        )

        await self._member["msg"].edit(embed = new_embed)

        self._new_specs = self._specs

    def __lvl_up(self):
        # Реализовать lvlUP параметров new_specs
        self._specs["lvl"] += 1
        self._specs["exp"] -= 100
        self._specs["crt"] = 10 + self._specs["lvl"]*5
        self._specs["dmg"] = int(20 + self._specs["lvl"]*1.2)

    def __str__(self):
        return f"{self._member['name']} [{self._specs['lvl']} lvl]  "


async def fight(f1:Fighter=None, f2:Fighter=None):
    # true f1   =>  false  f2
    turn = True

    while f1.can_fight and f2.can_fight:
        await asyncio.sleep(2)
        # Первый претендент
        if turn:
            turn = False
            await f1.attack(f2)
        # Вторый претендент
        else:
            turn = True
            await f2.attack(f1)
    
    # Выбор победиля
    if f1.can_fight:
        await f1.win(f2)
    else:
        await f2.win(f1)



async def create_fighters(f1:discord.Member, f2:discord.Member, message:discord.Message):
    f1_data = {
        "member": {
            "id": f1.id,
            "name": f1.display_name,
            "msg" : message
        },

        "specs": {
            "lvl": f1.id,
            "hp": 100 + f1.id*10,
            "exp": 0,
            "crt": 10 + f1.id*5,
            "dmg": int(20 + f1.id*1.2),
        },
    }

    f2_data = {
        "member": {
            "id": f2.id,
            "name": f2.display_name,
            "msg" : message
        },

        "specs": {
            "lvl": f2.id,
            "hp": 100 + f2.id*10,
            "exp": 0,
            "crt": 10 + f2.id*5,
            "dmg": int(20 + f2.id*1.2),
        },
    }

    fighter1 = Fighter(f1_data["member"], f1_data["specs"])
    fighter2 = Fighter(f2_data["member"], f2_data["specs"])

    await fight(fighter1, fighter2)


