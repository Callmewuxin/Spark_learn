from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
db = conn.spark #连接mydb数据库，没有则自动创建
hero = db.hero
biography = db.biography
story = db.story

hero_index = {}
hero_index_2 = {}
for id, name1, name2, loc in hero:
    hero_index[name1] = id
    hero_index_2[name2] = id

biography_list = [(x["biography"], x["title"]) for x in biography.find({}, {"_id":0, "biography":1, "title":1})]
hero_relation_biography = {}
for content, title in biography_list:
    hero_contain = []
    for hero_name1 in hero_index:
        if hero_index[hero_name1] == hero_index_2[title]:
            continue
        if hero_name1 in content:
            cnt = content.count(hero_name1)
            for c in range(cnt):
                hero_contain.append(hero_index[hero_name1])
    for hero_name2 in hero_index_2:
        if hero_index_2[hero_name2] == hero_index_2[title]:
            continue
        if hero_name2 in content:
            cnt = content.count(hero_name2)
            for c in range(cnt):
                hero_contain.append(hero_index_2[hero_name2])
    if len(hero_contain)>0:
        hero_relation_biography[hero_index_2[title]] = hero_contain
relation_bio = []
for k,v in relation_biography.items():
    for item in v:
        relation_bio.append((k,item))
        relation_bio.append((item, k))




	
