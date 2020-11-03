from invert import get_file_data
from nltk.stem import PorterStemmer
from search import search
from colorama import init, AnsiToWin32
import sys

init(wrap=False)
stream = AnsiToWin32(sys.stderr).stream
stop_words = get_file_data("common_words"," ")[0].split(" ")

def eval_map(docs,rel_docs):
    rels = [str(int(x)) for x in rel_docs]
    retrieved = [x["id"] for x in docs]
    rel_rev_intersect = [x for x in rels if x in retrieved]
    precision = []
    count = 0
    if not len(retrieved) == 0:
        for doc_index in range(len(retrieved)):
            if retrieved[doc_index] in rel_rev_intersect:
                count += 1
                precision.append(count/(doc_index + 1))
        return sum(precision)/len(rels)
    return 0

def eval_r_precision(docs,rel_docs):
    rels = [str(int(x)) for x in rel_docs]
    retrieved = [x["id"] for x in docs]
    rel_rev_intersection = [x for x in rels if x in retrieved]
    if len(retrieved) <= 0:
        return 0
    temp_len = len(rel_rev_intersection)
    index = 0
    count = 0
    for item in range(len(retrieved)):
        if count == temp_len:
            index = item + 1
            break
        else:
            if retrieved[item] in rel_rev_intersection:
                count += 1
    if index == 0:
        return 0
    return temp_len/index

def split_query_text(is_stem,is_stopword,eval_list):
    query_text = get_file_data("query.text",".I")
    eval_l = [str(int(x)) for x in eval_list]
    q_text = []
    for item in query_text:
        temp_dict = dict()
        temp = (item.replace(".W", "REMOVE_HERE").replace(".N", "REMOVE_HERE.N").replace(".A", "REMOVE_HERE.A")).split("REMOVE_HERE")
        temp_item = [x.strip() for x in temp if not x == '']
        if temp_item[0] in eval_l:
            temp_dict["id"] = temp_item[0]
            temp_dict["context"] = temp_item[1] 
            temp_dict["author"] = temp_item[2] if temp_item[2][:3] == ".A" else ""
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

# qrels has less query than the query.text
def eval(is_stem,is_stopword):
    rel_docs = split_query_a()
    list_of_index = [x for x in rel_docs]
    queries = split_query_text(is_stem,is_stopword,list_of_index)
    count = 0
    r_precision_sum = 0
    map_precision_sum = 0
    for query in queries:
        temp_res = search(query["context"],is_stem,is_stopword)
        r_precision = eval_r_precision(temp_res,rel_docs[list_of_index[count]])
        map_precision = eval_map(temp_res,rel_docs[list_of_index[count]])
        count += 1
        print("\033[1;32;40m ======================= \033[0;0m", file = stream)
        print("\033[1;32;40m Query : \033[0;0m{}".format(query["context"]), file = stream)
        print("R-Precision :\t\t\t{}".format(r_precision))
        print("Mean average precision :\t{}".format(map_precision))
        r_precision_sum += r_precision
        map_precision_sum += map_precision
    print("\033[1;32;40m =========== Summary =========== \033[0;0m", file = stream)
    print("Average R-Precision :\t\t\t{}".format(r_precision_sum/len(queries)))
    print("Average Mean average precision :\t{}".format(map_precision_sum/len(queries)))
    print("\033[1;32;40m =============================== \033[0;0m", file = stream)

eval(True,True)