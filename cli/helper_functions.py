import string
import json
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()


def tokenize(input: str):
    result=input.split()
    if "" in result:
        result.remove("")
    return result

def preprocess(input_string: str):
    trans_table = str.maketrans("","",string.punctuation)
    argument = input_string.translate(trans_table).lower()
    return argument

def transform_tokenized(imput: str, list_stop: list):
    argument = preprocess(imput)
    filtered_args=[]
    for thing in tokenize(argument):
        if thing not in list_stop:
            filtered_args.append(stemmer.stem(thing))
    return filtered_args

def stop_words(path: str):
    list_stop=[]
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
        for word in content.splitlines():
            list_stop.append(preprocess(word))
    return list_stop

def load_movies():
    with open("data/movies.json","r") as file:
        movie_dict=json.load(file)["movies"]
    return movie_dict