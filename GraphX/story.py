from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
db = conn.spark #连接mydb数据库，没有则自动创建
hero = db.hero
biography = db.biography
story = db.story
l = [x["story"] for x in story.find({}, {"_id":0, "story":1 })]
hero_relation_story = []
for t in l:
	hero_index = []
	for h in hero:
		if h[1] in t or h[2] in t:
			hero_index_syory.append(h[0])
	if len(hero_index)!=0 and len(hero_index)!=1:
		hero_relation_story.append(hero_index)

relation_story = []
for t in hero_relation_story:
    relation_story += list(itertools.combinations(t, 2))
relation_full = []
for k, v in relation_story:
    relation_full.append((k,v))
    relation_full.append((v,k))
relation = relation_bio + relation_full
relation_write = [' '.join(t) for t in relation]
relation_write = '\n'.join(relation_write)
with open("relation.txt", 'w') as relation_handle:
    relation_handle.write(relation_write)
