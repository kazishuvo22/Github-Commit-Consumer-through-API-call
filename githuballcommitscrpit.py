# -*- coding: utf-8 -*-
"""
Author: Kamruzzman Shuvo
Github Commit Consumer through api call
"""
import requests
import os, glob
from github import Github
from tqdm import tqdm
import pandas as pd
import json
import shutil

access_token = input("Enter Your User or Organization Github Token: ")
g = Github(access_token)
repo_list = [i for i in g.get_user().get_repos()]
for i in tqdm(repo_list):
    repo_name = str(i).replace('Repository(full_name="', '')
    repo_name = str(repo_name).replace('")', '')
    x = repo_name.split("/")
    owner = x[0]
    repo = x[1]
    query_url = f"https://api.github.com/repos/{owner}/{repo}/commits?sha=master"
    params = {
        "state": "open",
    }
    headers = {'Authorization': f'token {access_token}'}
    r = requests.get(query_url, headers=headers, params=params)
    
    if not os.path.exists('jsonTemp'):
        os.makedirs('jsonTemp')
    
    file  = open("jsonTemp/"+repo+".json","w")
    file.write(r.text)
    file.close()
print("Write all data Successfully")
#     print('https://www.github.com/' + repo_name)



json_files= glob.glob(os.path.join("jsonTemp/",'*.json'))
print(len(json_files))

for i in tqdm(json_files[:]):
    try:
        with open(i, 'r') as j:
            data = json.loads(j.read())
            for s in range(len(data)):
                df_nested_list = pd.json_normalize(data[s]['commit'])
                if os.path.exists('my_csv.csv'):
                    append_write = 'a' # append if already exists
                    head = False
                else:
                    append_write = 'w' # make a new file if not
                    head = True
                df_nested_list.to_csv('my_csv.csv', mode=append_write, header=head)
    except:
        print('No commit/ Commit Error!! on '+ i)


try:
    shutil.rmtree('jsonTemp')
except OSError as e:
    print("Error: %s : %s" % (dir_path, e.strerror))

print('Done!!!!!!')


