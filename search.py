import json
from nltk import PorterStemmer
from invert import get_file_data
import re
import math

def load_file(filename):
  return json.loads(open(filename, "r").read())  

ps = PorterStemmer()
doc_list = load_file("posting.json")
word_dict = load_file("dictionary.json")
lookup_dict = load_file("lookup.json")
stop_words = get_file_data("common_words"," ")[0].split(" ")

def query_filtering(query,is_stem,is_stopwords):
    temp_query_words = [re.sub('[^A-Za-z0-9]+', '', x) for x in query]
    query_words = [x.lower() for x in temp_query_words if not x == '']
    if is_stem:
        query_words = [ps.stem(x) for x in query_words if x not in stop_words] if is_stopwords else [ps.stem(x) for x in query_words]
    else:
        query_words = [x for x in query_words if x not in stop_words] if is_stopwords else query_words
    query_words = [x for x in query_words if x in word_dict]
    return query_words
def relavance_doc_retrieval(query_words):
    result, relavance_doc = [], []
    for word in query_words:
        relavance_doc += lookup_dict[word] if word in lookup_dict else []
    temp = {i:relavance_doc.count(i) for i in relavance_doc}
    result = [x for x in temp if temp[x] > 1]
    extra = [x for x in temp if temp[x] < 2]
    if len(extra) > 0:
        for word in query_words:
            temp_data =  [doc for doc in extra if word in doc_list[doc]["word_count"] and doc_list[doc]["word_count"][word] > 1]
        result += temp_data
    return sorted(set(result))

def doc_ranking(docs_id,data,query_words,original_query):
    rel_collection = []
    words_pool = []
    temp_wp = []
    ranking = []
    for key in docs_id:
        temp_wp += [x for x in data[key]["words_pool"]]
    words_pool = [x for x in temp_wp if x in word_dict]
    words_pool += query_words
    unique = sorted(set(words_pool))
    doc_freq = dict()
    for word in unique:
        doc_freq[word] = words_pool.count(word)
    words_pool = sorted(set(words_pool))
    for key in docs_id:
        temp_dict = dict()
        temp_dict["id"] = key
        temp_dict["word_list"] = data[key]["word_count"]
        for word in words_pool:
            if not word in temp_dict["word_list"]:
                temp_dict["word_list"][word] = 0
        rel_collection.append(temp_dict)
    #Found all the frequency of all words
    idf = inverse_doc_freq(len(rel_collection),words_pool,doc_freq)
    for item in rel_collection:
        for key in idf:
            if not item["word_list"][key] <= 0:
                item["word_list"][key] = idf[key] * (1 + math.log(item["word_list"][key],10))
    query = query_vector(original_query,idf,words_pool)
    for item in rel_collection:
        item_data = dict()
        item_data["id"] = item["id"]
        item_data["cosine_sim"] = cosine_similarity(query,item["word_list"])
        ranking.append(item_data)
    return sorted(ranking, key = lambda i: i['cosine_sim'],reverse = True)

def query_vector(query_words,idf_collection,words_pool):
    result = dict()
    for word in words_pool:
        result[word] = query_words.count(word)
    for word in idf_collection:
        if not result[word] == 0:
            result[word] = 1 + math.log(result[word],10)
        result[word] = result[word] * idf_collection[word]
    return result

# finding idf
def inverse_doc_freq(collection_len,words_pool,doc_freq): 
    idf = dict()
    for word in words_pool:
        idf[word] = math.log(collection_len/doc_freq[word],10) if collection_len > 0 else 0
    return idf

def vector_length(vector):
    inner_sum = 0
    for key in vector:
        inner_sum += vector[key]**2 if not key == 'id' else 0
    if inner_sum == 0:
        for key in vector:
            if not vector[key] == 0:
                print(key)
    return math.sqrt(inner_sum)

def cosine_similarity(query_v,doc_v):
    numerator = 0
    denominator = vector_length(query_v) * vector_length(doc_v)
    for key in query_v:
        numerator += query_v[key]*doc_v[key]
    return numerator/denominator

def single_term_dict(query,docs,is_stem,is_stopwords):
    r_query = ps.stem(query) if is_stem else query
    r_query = ps.stem(query) if is_stopwords  else r_query
    retrieved_docs = []
    for index in docs:
        temp_word_list = docs[index]["words_pool"]
        if query in temp_word_list:
            temp_dict = dict()
            temp_dict["id"] = docs[index]["id"]
            retrieved_docs.append(temp_dict)
    return retrieved_docs

def search(query,is_stem,is_stopwords):
    temp_query = [x for x in query.split(" ") if not x == '']
    if len(temp_query) > 1:
        unfiltered = query_filtering(temp_query,is_stem,is_stopwords)
        query_words = sorted(set(unfiltered))
        doc_id = relavance_doc_retrieval(query_words)
        return doc_ranking(sorted(set(doc_id)),doc_list,query_words,unfiltered)
    else:
        return single_term_dict(temp_query[0],doc_list,is_stem,is_stopwords)
