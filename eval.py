from invert import get_file_data
from nltk.stem import PorterStemmer
'''
The final part of the assignment is to evaluate the performance of the IR system you have developed. You need to write a program eval. 
The input to this program would be query.text and qrels.text from CACM. Your program should go through all the queries in query.text, for each query, 
get all the relevant results from your system (by running search), compare the results with the actual user judgment from qrels.text, and then calculate 
the mean average precision (MAP) and R-Precision values. The final output will be the average MAP and R-Precision values over all queries.
'''
# query.text and qrels.text
# MAP, R-precision

stop_words = get_file_data("common_words"," ")[0].split(" ")

def eval_map(docs,queries):
    precision = 0
    return precision

def eval_r_precision(docs,rel_docs):
    rels = [x for x in rel_docs]
    retrieved = [docs[x]["id"] for x in docs]
    rel_rev_intersection = [x for x in rels if x in retrieved]
    return len(rel_rev_intersection)/len(retrieved)

def split_query_text(is_stem,is_stopword):
    query_text = get_file_data("query.text",".I")
    q_text = []
    for item in query_text:
        temp_dict = dict()
        temp = (item.replace(".W", "REMOVE_HERE .W").replace(".N", "REMOVE_HERE .N")).split("REMOVE_HERE")
        temp_item = [x.strip() for x in temp if not x == '']
        temp_dict["id"] = temp_item[0]
        temp_dict["context"] = temp_item[1]
        temp_dict["author"] = temp_item[2]
        q_text.append(temp_dict)
    return q_text

def split_query_a():
    qrel_text = get_file_data("qrels.text")
    q_eval_value = [x.split(" ") for x in qrel_text]
    current = ""
    evaluation_data = dict()
    for item in q_eval_value:
        if not current == item[0]:
            current = item[0]
            evaluation_data[current] = [item[1]]
        else:
            evaluation_data[current].append(item[1])
    return evaluation_data


def eval(retrieved_docs,is_stem,is_stopword):
    rel_docs = split_query_a()
    queries = split_query_text(is_stem,is_stopword)
    
    r_precision = eval_r_precision(retrieved_docs,rel_docs)
    map_precision = eval_map(retrieved_docs,queries)
    
