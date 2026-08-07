import argparse


from inverted_index import build_command, InvertedIndex

def main() -> None:       
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")
    subparsers.add_parser("build", help="Build movies inverted index")
    args = parser.parse_args()

    index_class = InvertedIndex()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            try:
                index_class.load()
            except FileNotFoundError:
                print("File not found")
                return
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
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()