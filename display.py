from invert import main, get_file_data
from search import search
from eval import eval
from os import system, name 
import json
from colorama import init, AnsiToWin32
import sys
init(wrap=False)
stream = AnsiToWin32(sys.stderr).stream
import time

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor
spinner = spinning_cursor()
def clear(): 
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear')

def list_docs(docid_list,docs):
    for i in docid_list:
        temp_call = docs[i["id"]]
        print("\033[1;32;40m ================================== \033[0;0m", file = stream)
        if "title" in temp_call:
            print("\033[1;32;40m=== Title ===\033[0;0m")
            print(temp_call["title"]) 
        if "abstract" in temp_call:
            print("\033[1;32;40m=== Abstract ===\033[0;0m")
            print(temp_call["abstract"])
        if "author" in temp_call:
            print("\033[1;32;40m=== Author ===\033[0;0m")
            print(temp_call["author"])
    print("\033[1;32;40mFound: {}\033[0;0m".format(len(docid_list)), file = stream)

for _ in range(20):
    sys.stdout.write(next(spinner))
    sys.stdout.flush()
    time.sleep(0.1)
    sys.stdout.write('\b')

clear()
is_stem = True
is_stopwords = True
main(is_stem,is_stopwords)

def load_file(filename):
  return json.loads(open(filename, "r").read())

clear()

while(True):
    print("\033[1;32;40m ====================================================================================================== \033[0;0m", file = stream)
    print("\033[1;32;40m | Simple search engine                                                                               |\033[0;0m", file = stream)
    print("\033[1;32;40m | 1, To search, type 'search' below and the query for searching documents                            |\033[0;0m", file = stream)
    print("\033[1;32;40m | 2, To quit: type 'ZZEND' or 'exit' or 'quit'                                                       |\033[0;0m", file = stream)
    print("\033[1;32;40m | 3, To clear screen, type 'cls' or 'clear'                                                          |\033[0;0m", file = stream)
    print("\033[1;32;40m | 4, To change setting, type 'setting'                                                               |\033[0;0m", file = stream)
    print("\033[1;32;40m | 5, To see sample of evaluation (R-Precision and Mean Average Precision), type 'eval'               |\033[0;0m", file = stream)
    print("\033[1;32;40m ====================================================================================================== \033[0;0m", file = stream)
    inp = input(">>> ")
    if inp == "ZZEND" or inp =='exit' or inp == 'quit':
        break
    elif inp == "search":
        while (True):
            print("\033[1;32;40m Type 'ss' to stop searching \033[0;0m")
            term = input(">>> Search here : ")
            
            print("\033[1;32;40m ================= Loading ================= \033[0;0m")
            list_docs(search(term,is_stem,is_stopwords),load_file("posting.json"))
    elif inp == "setting":
        print("Type number to toggle between mode")
        print("1. Stemming: {}".format(is_stem))
        print("2. Stop word removal: {}".format(is_stopwords))
        print("To get back, type 'back'.")
        while (True):
            option = input(">>> ")    
            if option == "1":
                is_stem = not is_stem
                print("success")
            elif option == "2":
                is_stopwords = not is_stopwords
                print("success")
            elif option == "back":
                break
            else:
                print("Invalid command")
            main(is_stem,is_stopwords)
        print("Saved setting")
    elif inp == "eval":
        print("\033[1;32;40m === List of queries and evaluation === \033[0;0m", file = stream)
        eval(is_stem,is_stopwords)
    elif inp == "cls" or inp == "clear":
        clear()
    else:
        print("Invalid command")

print("\033[1;32;40m ............ Ending ............ \033[0;0m", file = stream)
print("\033[1;32;40m ================================== \033[0;0m", file = stream)