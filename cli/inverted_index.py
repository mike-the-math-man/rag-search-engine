from helper_functions import  stop_words, load_movies, transform_tokenized, tokenize_single
import pickle
import collections


class InvertedIndex:
    def __init__(self):
        self.index = {} #token to set of doc_id  
        self.docmap = {} #doc_id to full doc object
        self.stop = stop_words("data/stopwords.txt")
        self.term_frequencies = {} #doc_ids to counter objects

    def __add_documents(self,doc_id,text):
        if doc_id not in self.term_frequencies:
            self.term_frequencies[doc_id]= collections.Counter()
        tokens = transform_tokenized(text,self.stop)
        for token in tokens:
            self.term_frequencies[doc_id][token]+=1
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
        with open("cache/term_frequencies.pkl", "wb") as f3:
            pickle.dump(self.term_frequencies ,f3)

    def load(self):
        with open("cache/index.pkl", "rb") as f:
            self.index  = pickle.load(f)
        with open("cache/docmap.pkl", "rb") as f2:
            self.docmap = pickle.load(f2)
        with open("cache/term_frequencies.pkl", "rb") as f3:
            self.term_frequencies = pickle.load(f3)

    def get_tf(self, doc_id, term):
        if doc_id not in self.term_frequencies:
            print("doc_id missing")
            return 0
        if term not in self.term_frequencies[doc_id]:
            print("term missing")
            return 0
        return self.term_frequencies[doc_id][term]

    def get_doc_f(self, term):
        term_single = tokenize_single(term)
        if term_single[0] not in self.index:
            print(term_single[0])
            print("term missing")
            return 0
        return len(self.index[term_single[0]])

def build_command():
    index_class = InvertedIndex()
    index_class.build()
    index_class.save()

