import time
import json
import os
import requests
from package.botapi import *
from player import PLAYER
import datetime
import random
import threading
from monster import *
grop_number = 123123213123123#这里填群号
send_msg(grop_number,str(datetime.datetime.now()) + "\n 2.0机器人已启动")
send_msg(grop_number,"""=================\n机器人2.0功能列表：\n菜单\n排行榜\n签到\n乞讨\n我的信息\n抢劫@被抢人\n更新数据保存功能""")
monster_pool = []
def create_monster_pool():
    #血量越高，出现的概率越低
    #排序monsters
    pass
     
#持续获取消息
already_recv = []
player_list = []
today_qiandao = []
today = datetime.datetime.now().day
def qiandao(msg):
    if (msg["data"]["messages"][-1]["message"] == "签到"):
        name = msg["data"]["messages"][-1]["sender"]["nickname"]
        if (name in today_qiandao):
            send_msg(grop_number,name + " 今天已经签到过了！")
            return
        for i in player_list:
            if (i.name == name):
                i.add_money(1000)
                i.add_exp(100)
                guanai = random.randint(0,1000)
                i.add_money(guanai)
                send_msg(grop_number,i.name + " 签到成功！\n金币+%s\n经验+%s\n群友的关爱币+%s" % (1000,100,guanai))
               
                
                today_qiandao.append(name)
                return
        else:
            #如果没有找到
            player = PLAYER(name,0,5,100,1,0)
            player_list.append(player)
            player.add_money(2000)
            player.add_exp(100)
            send_msg(grop_number,player.name + "已注册账户，签到成功！\n金币+%s\n经验+%s" % (2000,100))
            today_qiandao.append(name)
def qitao(msg):
    if (msg["data"]["messages"][-1]["message"] == "乞讨"):
        name = msg["data"]["messages"][-1]["sender"]["nickname"]
        for i in player_list:
            if (i.name == name ):
                if(i.money > 200):
                    send_msg(grop_number,i.name + " 你的金币太多了，无法乞讨！")
                    return
                coin = random.randint(1,200)
                i.add_money(coin)
                send_msg(grop_number,i.name + " 乞讨成功！\n金币+%s" % (coin))
                return
        else:
            send_msg(grop_number,name + " 你还没有签到，无法乞讨！")
def my_info(msg):
    if(msg["data"]["messages"][-1]["message"] == "我的信息"):
        name = msg["data"]["messages"][-1]["sender"]["nickname"]
        for i in player_list:
            if (i.name == name):
                send_msg(grop_number,i.name + " 你的信息如下：\n金币：%s\n经验：%s\n等级：%s\n攻击力：%s\n生命值：%s\n最大生命值：%s\n下一级经验%s" % (i.money,i.exp,i.level,i.attack,i.hp,i.max_hp,i.level*200))
                return
        else:
            send_msg(grop_number,name + " 你还没有注册账户！")
def rob(msg):
    name = ""
    by_rob_name = ""
    try:
        if("打劫" in msg["data"]["messages"][-1]["message"]):
            #打劫[CQ:at,qq=3066148636]
            name = msg["data"]["messages"][-1]["sender"]["nickname"]
            by_rob_name = msg["data"]["messages"][-1]["message"][3:-1]
            by_rob_id = by_rob_name.split("=")[1]
            if ("]" in by_rob_id):
                by_rob_id = by_rob_id[:-1]
            #by_rob_id 为被打劫者的qq号
            print(by_rob_id)
            by_rob_name = get_group_member_info(grop_number,by_rob_id)["data"]["nickname"]
            print(name,"打劫 ",by_rob_name)
            for i in player_list:
                if(i.name == name):#查找打劫者
                    print("找到打劫者")
                    for j in player_list:
                        if(j.name == by_rob_name):#查找被打劫者
                            print("找到被打劫者")
                            if(random.randint(1,3) ==1):
                                rob_coin = random.randint(1,(j.money//2))#被打劫者金币的一半
                                send_msg(grop_number,"%s 打劫%s成功！\n金币+%s" % (i.name,j.name,rob_coin))
                                i.add_money(rob_coin)
                                j.add_money(-rob_coin)
                                return
                            else:
                                lost_coin = random.randint(1,(i.money//6))#打劫者金币的1/6
                                send_msg(grop_number,"%s 打劫%s失败！,并且还被抢走了金币%s！" % (i.name,j.name,lost_coin))
                                i.add_money(-lost_coin)
                                j.add_money(lost_coin)               
    except:
        pass
def show_money_list(msg):
    if(msg["data"]["messages"][-1]["message"] == "排行榜"):
        #打印player_list中的所有玩家的信息，按照金币排序
        number = 0
        player_list.sort(key=lambda x:x.money,reverse=True)
        string ="财富排行榜：\n"
        for i in player_list:
            if number == 5:
                break
            number += 1
            string += i.name + " 金币：%s\n" % (i.money)
        send_msg(grop_number,string)
        #再打印一个战力排行榜
        player_list.sort(key=lambda x:x.attack,reverse=True)
        string ="战力排行榜：\n"
        number = 0
        for i in player_list:
            if number == 5:
                break
            number += 1
            string += i.name + " 战力：%s\n" % (i.attack)
        send_msg(grop_number,string)       
def show_menu(msg):
    if(msg["data"]["messages"][-1]["message"] == "菜单"):
        send_msg(grop_number,"菜单：\n签到\n乞讨\n我的信息\n打劫@被打劫号]\n排行榜\n背包\n使用物品#物品名\n打怪\n持续打怪(最多100次)\n补血\n使用全部物品\n装备回收")     
def show_backpack(msg):
    if(msg["data"]["messages"][-1]["message"] == "背包"):
        name = msg["data"]["messages"][-1]["sender"]["nickname"]
        for i in player_list:
            if (i.name == name):
                while(len(i.backpack) >= 50):
                    i.backpack.pop()#删除最后一个元素
                    
                send_msg(grop_number,i.name + " 你的背包如下：\n" + str(i.backpack))
                return
        else:
            send_msg(grop_number,name + " 你还没有注册账户！")            
def use_item(msg):
    if("使用物品#" in msg["data"]["messages"][-1]["message"]):
        name = msg["data"]["messages"][-1]["sender"]["nickname"]
        item_name = msg["data"]["messages"][-1]["message"][5:]
        print(item_name)
        for i in player_list:
            if (i.name == name):
               for j in i.backpack:
                    if(j == item_name):
                        if(item_name == "木剑"):
                            send_msg(grop_number,i.name + " 使用了%s！\n攻击力+1" % (item_name))
                            i.add_attack(1)
                            i.del_item(item_name)
                            return
                        if (item_name == "铁剑"):
                            send_msg(grop_number,i.name + " 使用了%s！\n攻击力+10" % (item_name))
                            i.add_attack(10)
                            i.del_item(item_name)
                            return
                        if(item_name == "屠龙宝刀"):
                            send_msg(grop_number,i.name + " 使用了%s！\n攻击力+100" % (item_name))
                            i.add_attack(100)
                            i.del_item(item_name)
                            return
                        if(item_name == "经验书"):
                            send_msg(grop_number,i.name + " 使用了%s！\n经验+100" % (item_name))
                            i.add_exp(100)
                            i.del_item(item_name)
                            return
                        if(item_name == "生命水晶"):
                            send_msg(grop_number,i.name + " 使用了%s！\n最大生命+100" % (item_name))
                            i.add_max_hp(100)
                            i.del_item(item_name)
                            return
                        if(item_name == "生命药水"):
                            send_msg(grop_number,i.name + " 使用了%s！\n生命回满" % (item_name))
                            i.hp = i.max_hp
                            return
                        if(item_name == "篮球"):
                            send_msg(grop_number,"鸡你太美！")
                            i.del_item(item_name)
                            i.attack +=10
                        return
                    else:
                        send_msg(grop_number,name + " 你的背包中没有这个物品！")
        else:
            send_msg(grop_number,name + " 你还没有注册账户！")
def attack_monster(msg):
    
    if("打怪" == msg["data"]["messages"][-1]["message"]):
        name = msg["data"]["messages"][-1]["sender"]["nickname"]   
        for i in player_list:
            if(i.name == name):
                if (i.hp <= 0):
                    send_msg(grop_number,"%s的血量为0，请补满血量再来" % (i.name))
                    return
                img_monster = random.choice(monsters)
                monster = Monster(img_monster)
                send_msg(grop_number,"%s 遇到了怪物【%s】!\n怪物的血量为%s\n怪物的攻击为%s\n%s的血量为%s\n%s的攻击力为%s\n" % (i.name,monster.name,monster.hp,monster.attack,i.name,i.hp,i.name,i.attack))
                while(i.hp > 0 and monster.hp > 0):
                    monster.hp -= i.attack
                    i.hp -= monster.attack
                if (i.hp <= 0):
                    send_msg(grop_number,"%s被打败了！\n请补满血量再来" % (i.name))
                    return
                else:
                    while(i.exp >= 200*i.level):
                        i.exp -= 200*i.level
                        i.level += 1
                        i.max_hp += 100
                        i.hp = i.max_hp
                        i.attack += 10
                        send_msg(grop_number,"%s升级了！\n等级提升为%s\n最大生命提升为%s\n攻击力提升为%s" % (i.name,i.level,i.max_hp,i.attack))
                    i.money += monster.money+random.randint(0,monster.money)
                    i.exp += monster.exp
                    drop_item = "[无]"
                    try:
                        if (random.randint(1,5) <=1):
                            drop_item = random.choice(monster.mightdrop)
                            i.add_backpack(drop_item)
                            print(i.backpack)
                    except Exception as e:
                       drop_item = "[错误]"+str(e)
                    send_msg(grop_number,"%s打败了怪物【%s】!\n获得了%s金币和%s经验\n%s掉落了%s" % (i.name,monster.name,monster.money,monster.exp,monster.name,drop_item))    
def buxue(msg):
     if(msg["data"]["messages"][-1]["message"] == "补血"):
        name = msg["data"]["messages"][-1]["sender"]["nickname"]
        for i in player_list:
            if(i.name == name):
                if(i.money < 200):
                    send_msg(grop_number,name + "你的金钱不足！")
                    return
                else:
                    i.money -= 200
                    i.hp = i.max_hp
                    send_msg(grop_number,name + "你的血量已经补满！目前内测优惠价200")
                    return
        else:
            send_msg(grop_number,name + " 你还没有注册账户！\n发送“签到”来注册！")
def continue_attack_monster(msg):
    """持续打怪 直到没血"""
    if("持续打怪" == msg["data"]["messages"][-1]["message"]):
        name = msg["data"]["messages"][-1]["sender"]["nickname"]   
        for i in player_list:
            if(i.name == name):
                if(i.hp <= 0):
                    send_msg(grop_number,"%s的血量不足，无法持续打怪！" % (i.name))
                    return
                send_msg(grop_number,"%s 持续打怪开始！" % (i.name))
                monster = Monster(random.choice(monsters))
                around = 0
                while(i.hp > 0):
                    if (around == 100):
                        send_msg(grop_number,"持续打怪结束，坚持了100轮,持续打怪结束！")
                        return
                    around += 1
                    monster.hp -= i.attack
                    i.hp -= monster.attack
                    if (i.hp <= 0):
                        send_msg(grop_number,"持续打怪结束，坚持了%s轮，%s被打败了！\n请补满血量再来" % (around,i.name))
                    if(monster.hp <= 0):#怪物死亡
                        while(i.exp >= 200*i.level):
                            i.exp -= 200*i.level
                            i.level += 1
                            i.max_hp += 100
                            i.hp = i.max_hp
                            i.attack += 10
                            #send_msg(grop_number,"%s升级了！\n等级提升为%s\n最大生命提升为%s\n攻击力提升为%s" % (i.name,i.level,i.max_hp,i.attack))
                        i.money += monster.money+random.randint(0,monster.money)
                        i.exp += monster.exp
                        drop_item = "[无]"
                        try:
                            if (random.randint(1,60) <=1):
                                drop_item = random.choice(monster.mightdrop)
                                i.add_backpack(drop_item)
                                #print(i.backpack)
                        except Exception as e:
                           drop_item = "[错误]"+str(e)
                        #send_msg(grop_number,"%s打败了怪物【%s】!\n获得了%s金币和%s经验\n%s掉落了%s" % (i.name,monster.name,monster.money,monster.exp,monster.name,drop_item))
                        monster = Monster(random.choice(monsters))
def use_item_all(msg):
    #使用背包中全部物品
    if("使用全部物品" in msg["data"]["messages"][-1]["message"]):
        name = msg["data"]["messages"][-1]["sender"]["nickname"]
        for i in player_list:
            if(i.name == name):
                if i.backpack == []:
                    send_msg(grop_number,name + " 背包中没有物品！")
                    return
                for item_name in i.backpack:
                    if(item_name == "木剑"):
                        send_msg(grop_number,i.name + " 使用了%s！\n攻击力+1" % (item_name))
                        i.add_attack(1)
                        i.del_item(item_name)
                        
                    if (item_name == "铁剑"):
                        send_msg(grop_number,i.name + " 使用了%s！\n攻击力+10" % (item_name))
                        i.add_attack(10)
                        i.del_item(item_name)
                        
                    if(item_name == "屠龙宝刀"):
                        send_msg(grop_number,i.name + " 使用了%s！\n攻击力+100" % (item_name))
                        i.add_attack(100)
                        i.del_item(item_name)
                        
                    if(item_name == "经验书"):
                        send_msg(grop_number,i.name + " 使用了%s！\n经验+100" % (item_name))
                        i.add_exp(100)
                        i.del_item(item_name)
                        
                    if(item_name == "生命水晶"):
                        send_msg(grop_number,i.name + " 使用了%s！\n最大生命+100" % (item_name))
                        i.add_max_hp(100)
                        i.del_item(item_name)
                        
                    if(item_name == "生命药水"):
                        send_msg(grop_number,i.name + " 使用了%s！\n生命回满" % (item_name))
                        i.hp = i.max_hp
                        
                    if(item_name == "篮球"):
                        send_msg(grop_number,"鸡你太美！")
                        i.del_item(item_name)
                        i.attack +=10
                        
def save_player():
    #保存玩家信息
    #每分钟保存一次
    if player_list == []:
        print("没有玩家信息！")
        return
    for i in player_list:
        print(i.name,i.money,i.attack,i.hp,i.level,i.exp,i.backpack)
        with open("players/"+str(i.name)+".json","w",encoding="utf-8") as f:
            f.write(json.dumps({"name":i.name,"money":i.money,"attack":i.attack,"hp":i.hp,"max_hp":i.max_hp,"level":i.level,"exp":i.exp,"backpack":i.backpack}))
            print("保存成功！"+i.name)
def read_player():
    
    print("读取玩家信息中...")
    #读取players文件夹中所有的玩家信息
    for root, dirs, files in os.walk("players"):
        #读取每个文件的内容
        for file in files:
            with open(os.path.join(root, file), 'r',encoding="utf-8") as f:
                #将json格式的字符串转换为python对象
                a = json.loads(f.read())
                b = PLAYER("a",0,0,0,0,0)
                b.name = a["name"]
                b.attack = a["attack"]
                b.money = a["money"]
                b.attack = a["attack"]
                b.level = a["level"]
                b.exp = a["exp"]
                b.hp = a["hp"]
                b.max_hp = a["max_hp"]
                b.backpack = a["backpack"]
                player_list.append(b)
                print("读取成功！"+b.name)
def recycel_item(msg):
    """装备回收"""
    #回收当前角色仓库中所有的装备，回收后获得一定的金钱
    coin = 0
    if(msg["data"]["messages"][-1]["message"] == "回收装备" or msg["data"]["messages"][-1]["message"] == "装备回收"):
        name = msg["data"]["messages"][-1]["sender"]["nickname"]
        for i in player_list:
            if (i.name == name):
                while(len(i.backpack) >= 50):
                    i.backpack.pop()#删除最后一个元素
                for item_name in i.backpack:
                    if(item_name == "木剑"):
                        coin += 10
                        continue
                    if (item_name == "铁剑"):
                        coin += 100
                        continue
                    if(item_name == "屠龙宝刀"):
                        coin += 1000
                        continue
                    if(item_name == "经验书"):
                        coin += 100
                        continue
                    if(item_name == "生命水晶"):
                        coin += 100
                        continue
                    if(item_name == "生命药水"):
                        coin += 100
                        continue
                    if(item_name == "篮球"):
                        coin += 100
                        continue
                i.backpack = []
                i.money += coin
                send_msg(grop_number,i.name + " 回收了所有的装备！\n获得了%d金币！" % (coin))
def guaguale(msg):
    """刮刮乐""" 
    taglist = "富强民主文明和谐自由平等"
    tag = ""
    if("刮刮乐" == msg["data"]["messages"][-1]["message"]):
        name = msg["data"]["messages"][-1]["sender"]["nickname"]
        print(name + "使用了刮刮乐！")
        for i in player_list:
            if(i.name == name):
                if(i.money < 1000):
                    send_msg(grop_number,i.name + " 金币不足！")
                    return
                i.money -= 1000
                
                for j in range(5):
                    tag+=random.choice(taglist)
                send_msg(grop_number,i.name + " 使用了1000金币！购买了一张[爱国刮刮乐]！\n刮刮乐上的字是：\n=================\n" + tag+"\n=================")
                #判断是否中奖
                #如果有三个相同的字，就中奖 5000 如果有4个相同的字，就中奖 10000 如果有5个相同的字，就中奖 100000
                already_count = []
                for k in tag:
                    #统计每个字出现的次数
                    if k in already_count:
                        continue
                    a = tag.count(k)
                    if a == 3:
                        send_msg(grop_number,i.name + " 中奖了！获得了5000金币！")
                        i.money += 5000
                    if a == 4:
                        send_msg(grop_number,i.name + " 中奖了！获得了10000金币！")
                        i.money += 10000
                    if a == 5:
                        send_msg(grop_number,i.name + " 中奖了！获得了100000金币！")
                        i.money += 100000
                
create_monster_pool()

read_player()

    
while True:
    #print(player_list)
    try:
        if (datetime.datetime.now().day != today):
            today_qiandao = []
            today = datetime.datetime.now().day
            
        if (len(already_recv) > 100):
            already_recv = []
        msg = get_group_msg_history(grop_number,0)
        if (msg["data"]["messages"][-1] in already_recv):
            continue
        #如果是limbo发送的消息，就跳过
        if (msg["data"]["messages"][-1]["sender"]["nickname"] == "limbo"):#机器人的昵称
            continue
        already_recv.append(msg["data"]["messages"][-1])
        
        t1 = threading.Thread(target=qiandao,args=(msg,))
        t1.start()
        t2 = threading.Thread(target=qitao,args=(msg,))
        t2.start()
        t3 = threading.Thread(target=my_info,args=(msg,))
        t3.start()
        t4 = threading.Thread(target=rob,args=(msg,))
        t4.start()
        t5 = threading.Thread(target=show_money_list,args=(msg,))
        t5.start()
        t6 = threading.Thread(target=show_menu,args=(msg,))
        t6.start()
        t7 =threading.Thread(target=show_backpack,args=(msg,))
        t7.start()
        t8 = threading.Thread(target=use_item,args=(msg,))
        t8.start()
        t9 = threading.Thread(target=attack_monster,args=(msg,))
        t9.start()
        t10 = threading.Thread(target=buxue,args=(msg,))
        t10.start()
        t11 = threading.Thread(target=continue_attack_monster,args=(msg,))
        t11.start()
        t12 = threading.Thread(target=use_item_all,args=(msg,))
        t12.start()
        t13 = threading.Thread(target=recycel_item,args=(msg,))
        t13.start()
        t14 = threading.Thread(target=guaguale,args=(msg,))
        t14.start()
        save_player()
    except Exception as e:
        print(e)
        save_player()    
    
