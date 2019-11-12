from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
db = conn.spark #连接mydb数据库，没有则自动创建
hero = db.hero
biography = db.biography
story = db.story
l = [(x["name"], x["title"], x["faction_cn"]) for x in hero.find({}, {"_id":0, "name":1, "faction_cn":1, "title":1})]
cnt = 0
hero = []
for i, t in enumerate(l):
    hero.append((str(1000+i), t[0], t[1], t[2])) #生成id，名字和地区
hero_write = [' '.join(t) for t in hero]
hero_write = '\n'.join(hero_write)
with open("hero.txt", 'w', encoding='UTF-8') as f: # 写入文件
    f.write(hero_write)

hero_rdd = sc.textFile("hdfs://master:9000/user/hadoop/hero.txt")