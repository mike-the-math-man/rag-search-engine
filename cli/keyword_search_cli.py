import argparse
import json
from nltk.stem import PorterStemmer

from helper_functions import  transform_tokenized,stop_words

def main() -> None:
    with open("data/movies.json","r") as file:
        movie_dict=json.load(file)

        list_stop = stop_words("data/stopwords.txt")

        stemmer = PorterStemmer()
        
        parser = argparse.ArgumentParser(description="Keyword Search CLI")
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        search_parser = subparsers.add_parser("search", help="Search movies using keywords")
        search_parser.add_argument("query", type=str, help="Search query")
        args = parser.parse_args()

        match args.command:
            case "search":
                print(f"Searching for: {args.query}")
                matching=[]
                for movie in movie_dict["movies"]:
                    filtered_args = transform_tokenized(args.query,list_stop)
                    filtered_titles = transform_tokenized(movie["title"],list_stop)
                    for word in filtered_args:
                        for title in filtered_titles:
                            if stemmer.stem(word) in stemmer.stem(title):
                                if movie["title"] not in matching:
                                    matching.append(movie["title"])
                for i in range(5 if len(matching)>5 else len(matching)):
                    print(f"{i+1}. {matching[i]}\n")
            case _:
                parser.print_help()


if __name__ == "__main__":
    main()