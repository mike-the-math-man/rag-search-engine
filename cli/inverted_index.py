from helper_functions import  stop_words, load_movies, transform_tokenized
import pickle



class InvertedIndex:
    def __init__(self):
        self.index = {} #token to set of doc_id  
        self.docmap = {} #doc_id to full doc object
        self.stop = stop_words("data/stopwords.txt")

    def __add_documents(self,doc_id,text):
        tokens = transform_tokenized(text,self.stop)
        for token in tokens:
            if token not in self.index:
                self.index[token]=set()
            self.index[token].add(doc_id)

    def get_documents(self, term):
        sanitized_term_list = transform_tokenized(term,self.stop)
        list_of_ids = []
        for item in sanitized_term_list:
            set_of_ids = self.index.get(item,set())
            ids = list(set_of_ids)
            for id in ids:
                list_of_ids.append(id)
        list_of_ids.sort()
        return list_of_ids

    def build(self):
        movie_dict = load_movies()
        for movie in movie_dict:
            doc_id = movie["id"]
            self.docmap[doc_id]=movie
            self.__add_documents(doc_id,text=f"{movie['title']} {movie['description']}")

    def save(self):
        with open("cache/index.pkl", "wb") as f:
            pickle.dump(self.index,f)
        with open("cache/docmap.pkl", "wb") as f2:
            pickle.dump(self.docmap,f2)

    def load(self):
        with open("cache/index.pkl", "rb") as f:
            index = pickle.load(f)
        with open("cache/docmap.pkl", "rb") as f2:
            docmap = pickle.load(f2)
        self.index = index
        self.docmap = docmap

def build_command():
    index_class = InvertedIndex()
    index_class.build()
    index_class.save()

