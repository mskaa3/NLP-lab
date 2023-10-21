from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
import pandas as pd
import os
from tqdm import tqdm
from const import DATA_PATH, NUM_PAGES, WYKOP_URL,DATE


tags=["Polska"]
users=[]
data=[]

for tag in tags:
    for i in range(1, NUM_PAGES):
        if i == 1:
            r=requests.get(WYKOP_URL+tag)
        else:
            r=requests.get(WYKOP_URL+tag+"/strona/"+str(i))
        soup=BeautifulSoup(r.text, "html.parser")
        all_posts=soup.find_all("section")
        for post in all_posts:
                print("tag: ", tag, "page: ", i)
                # about posts
                if post.get("class") == ["entry"]:
                    main_post_id=post.get("id").split("-")[-1]
                    try:
                        main_post = post.find_all("article",limit=1)[0]
                        name = main_post.find("a",class_="avatar")
                        date = main_post.find("time")
                        content = main_post.find("div",class_="wrapper")
                        rating = main_post.find("li",class_="plus")
                        comments = main_post.find("a",class_="comment-counter")
                        
                        
                        name=name.get("href").split("/")[-1]
                        date=date.get("datetime")

                        content=content.get_text()           
                        comments=comments.get_text() if comments != None else "0"
                        rating=rating.get_text() if rating != None else "0"

                        new_date = datetime.strptime(date.split(" ")[0], '%Y-%m-%d').date()
                        if new_date > DATE:
                            if name not in users:
                                users.append(name)
                            single_data={
                                        "post_id" :int(main_post_id),
                                        "author":str(name),
                                        "date":str(date),
                                        "content":str(content),
                                        "tag":tag,
                                        "rating" : int(rating),
                                        "comments" : int(comments.replace(" ","")),
                                        "is_reply": False,
                                        "replies_to": None
                                }
                            if single_data not in data:
                                data.append(single_data)

                            # post replies
                            reply_comments=post.find_all("section")

                            for reply in reply_comments:
                                    if reply.get("class") == ["entry", "reply"]:
                                        reply_id=reply.get("id").split("-")[-1]
                                        name = reply.find("a",class_="avatar")
                                        date = reply.find("time")
                                        content = reply.find("div",class_="wrapper")
                                        rating = reply.find("li",class_="plus")

                                        name=name.get("href").split("/")[-1]
                                        date=date.get("datetime")
                                        content=content.get_text()
                                        rating=rating.get_text() if rating != None else "0"
                                        if name not in users:
                                            users.append(name)
                                        single_data={
                                                "post_id" :int(reply_id),
                                                "author":str(name),
                                                "date":str(date),
                                                "content":str(content),
                                                "tag":tag,
                                                "rating" : int(rating),
                                                "comments" : 0 ,
                                                "is_reply": True,
                                                "replies_to": main_post_id
                                        }
                                        if single_data not in data:
                                            data.append(single_data)
                
                    except:
                        pass



df = pd.DataFrame(data) 
df.to_csv(os.path.join(DATA_PATH, f"wykop_data_{NUM_PAGES}_pages.csv"))

with open(os.path.join(DATA_PATH, f"wykop_data_{NUM_PAGES}_pages.json"), "w",encoding='utf8') as f:
    json.dump(data, f,ensure_ascii=False)
with open(os.path.join(DATA_PATH, f"wykop_metadata_{NUM_PAGES}_pages.json"), "w",encoding='utf8') as f:
    json.dump({"number_of_users":len(users), "number_of_posts": len(data), "number_of_tags": len(tags)}, f,ensure_ascii=False)
