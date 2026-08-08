import argparse

from helper_functions import tokenize_single
from inverted_index import build_command, InvertedIndex
import math

def main() -> None:       
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")
    subparsers.add_parser("build", help="Build movies inverted index")
    tf_parser = subparsers.add_parser("tf", help="term frequency search - ID and a term as arguments")
    tf_parser.add_argument("ID", type=str, help="document ID")
    tf_parser.add_argument("term", type=str, help="search term")
    idf_parser = subparsers.add_parser("idf", help="calculate idf for one term")
    idf_parser.add_argument("idf_term", type=str, help="search term")
    args = parser.parse_args()

    index_class = InvertedIndex()
    try:
        index_class.load()
    except FileNotFoundError:
        print("File not found")
        return
    #print(index_class.index["grizzly"])
    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            
            matching=set()
            for id in index_class.get_documents(args.query):  #was word
                matching.add(id)
                if len(matching)>4:
                    break
            matching = list(matching)
            matching.sort()
            for i in range(len(matching)):  
                print(f"{matching[i]}. {index_class.docmap[matching[i]]['title']}\n")
        case "build":
            build_command()
        case "tf":
            print(f"Searching for: {args.ID} and {args.term}")
            term_single = tokenize_single(args.term)
            term_frequency = index_class.get_tf(int(args.ID),term_single[0])
            print(term_frequency)
        case "idf":
            print(f"Searching for: {args.idf_term}")
            term_idf = math.log((len(index_class.docmap) + 1) / (index_class.get_doc_f(args.idf_term) + 1))
            print(f"Inverse document frequency of '{args.idf_term}': {term_idf:.2f}")        
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()