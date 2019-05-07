import pandas as pd 
import numpy as np 
import ast
import json
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

'''
This file is for preprocessing our data. 
We removed irrelevant columns, and modified others to make data more easily parsed.
We will save the data to a new csv file to be used with our methods.

'''



def text_to_list(x):
    if pd.isna(x):
        return ''
    else:
        return ast.literal_eval(x)

def parse_json(x):
    try:
        return json.loads(x.replace("'", '"'))[0]['name']
    except:
        return ''


def main():
    full_data = pd.read_csv('train.csv')
    
    y = full_data['genres']

    x = full_data.drop(columns=['genres', 'id', 'imdb_id', 'poster_path', 'homepage', 'production_countries', 'status', 'original_title', 'spoken_languages'], axis = 1)

    # make target rows into a list
    y = y.apply(parse_json)
    y = y.apply(text_to_list)

    # parse crew, save director and producer to new columns, delete crew column, insert director and producer columns.
    
    x["crew"] = x["crew"].fillna("")
    crew = x['crew']
    director = []
    producer = []
    for i in range(len(x)):
        # print(i)
        dir_name = ""
        pro_name = ""
        data = x['crew'][i]
        if data == "":
            director.append("")
            producer.append("")
            continue
        data_dict = ast.literal_eval(data)
        
        for cm in range(len(data_dict)):
            member = data_dict[cm]
            # find director
            if "job" not in member.keys():
                continue
            if member["job"] == "Director":
                dir_name = member["name"]
                break
            else:
                continue
        director.append(dir_name)
        
        for cm in range(len(data_dict)):
            member = data_dict[cm]
            # find producer
            if "job" not in member.keys():
                continue
            if member["job"] == "Producer":
                pro_name = member["name"]
                break
            else:
                continue
        producer.append(pro_name)
       
    x['director'] = director
    x['producer'] = producer

    # analyser = SentimentIntensityAnalyzer()
    x['overview'] = x['overview'].fillna('')
    x['tagline'] = x['tagline'].fillna('')

    for col in ['belongs_to_collection', 'production_companies', 'Keywords']:
        x[col] = x[col].apply(parse_json)
        x[col] = x[col].apply(text_to_list)
    
    x['belongs_to_collenction'] = 1*(~x['belongs_to_collection'].isna())

    print(x['belongs_to_collection'].head())

main()