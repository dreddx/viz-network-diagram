import json
import pandas as pd

CUTOFF = 200
actors = pd.read_csv('actor_labels.csv')
network = pd.read_csv('network_dataframe.csv')

frequency = {}
for idx, row in network.iterrows():
    if row["source"] in frequency:
        frequency[row["source"]] += 1
    else:
        frequency[row["source"]] = 1

frequency_df = pd.DataFrame.from_dict(frequency, orient='index')
frequency_df.reset_index(inplace=True)
frequency_df.columns = ['id','frequency']
frequency_df.sort_values(by='frequency',ascending=False,inplace=True)
frequency_df = frequency_df.iloc[:CUTOFF]

df = pd.read_csv('movies_network.csv')

actor_1 = df[['Actor 1','Rating']]
actor_1.rename(columns={'Actor 1':'Actor'},inplace=True)
actor_2 = df[['Actor 2','Rating']]
actor_2.rename(columns={'Actor 2':'Actor'},inplace=True)
actor_3 = df[['Actor 3','Rating']]
actor_3.rename(columns={'Actor 3':'Actor'},inplace=True)
actor_4 = df[['Actor 4','Rating']]
actor_4.rename(columns={'Actor 4':'Actor'},inplace=True)

actor_scores = pd.concat([actor_1,actor_2,actor_3,actor_4])

actor_scores = actor_scores.groupby('Actor').agg('mean')
actor_scores.reset_index(inplace=True)

def assign_group(label):

    score = actor_scores[actor_scores['Actor']==label]['Rating'].values[0]

    if score < 7.4:
        return 1
    if score < 7.6:
        return 2
    if score < 7.9:
        return 3
    if score >= 7.9:
        return 4
    else:
        return 0
    

nodes = []
for idx, row in actors.iterrows():
    if row["Id"] in frequency_df['id'].values:
        node = {
            "id": row["Id"],
            "label": row["Label"],
            "size": frequency_df[frequency_df['id'] == row["Id"]].frequency.tolist()[0],
            "group": assign_group(row["Label"])
        }
        nodes.append(node)

nodes_df = pd.DataFrame(nodes)
nodes_df.to_json("nodes.json",orient='records',lines=True)

# ------------------

# source,target
# 1,1802
links = []
for idx, row in network.iterrows():
    if row["source"] in frequency_df['id'].values and row["target"] in frequency_df['id'].values:
        link = {
            "source": row["source"],
            "target": row["target"]
        }
        links.append(link)

links_df = pd.DataFrame(links)
links_df.to_json("links.json",orient='records',lines=True)
