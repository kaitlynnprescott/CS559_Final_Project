import numpy as np
import pandas as pd
#for reading in data properly
import ast
import json

all_data = pd.read_csv('train.csv')

genre_set = {'Comedy'}#set of all unique genres in dataset
genre_dict = {}#maps genre string to id (index label vector)


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

def parse_all_genres_json(x):
    try:
        json_genres = json.loads(x.replace("'", '"'))
        numElems = len(json_genres)
        for i in range(numElems):
            genre_set.add(json_genres[i]['name'])
    except:
        return ''

def parse_genres_json(x):
    try:
        json_genres = json.loads(x.replace("'", '"'))
        numElems = len(json_genres)
        ret = [0]*len(genre_dict) #20 0s
        for i in range(numElems):
            ret[genre_dict[(json_genres[i]['name'])]] = 1
        return ret
    except:
        return ''

def getAllGenres():
    full_data = pd.read_csv('train.csv')

    y = full_data['genres']
    y.apply(parse_all_genres_json)


#get set to dictionary for indexing of target vectors
def getGenreDict():
    index = 0
    for genre in genre_set:
        genre_dict[genre] = index
        index += 1

def getGenresVect():
    y = all_data['genres']
    y = y.apply(parse_genres_json)
    return y

#main
getGenreDict()
print(genre_dict)
print()
print(getGenresVect())
