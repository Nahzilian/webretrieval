from nltk.stem import PorterStemmer 
import json
from invert import main, get_file_data
from nltk.tokenize import word_tokenize
import re
from colorama import init, AnsiToWin32

is_stem = True
is_stopwords = True
term = ""
main(is_stem,is_stopwords)
stop_words = get_file_data("common_words"," ")[0].split(" ")

def load_file(filename):
  return json.loads(open(filename, "r").read())

def get_data(data, inp):
  for key in data:
    count = 0
    is_found = False
    if "title" in data[key]:
      if inp in data[key]["title"]:
        print("\033[1;32;40m- ID:\033[0;0m\t {}".format(data[key]["id"]))
        if "title" in data[key]:
          print("\033[1;32;40m- Title:\033[0;0m\t {}".format(data[key]["title"]))
        else:
          print("\033[1;32;40m ---No title given--- \033[0;0m") 
        if inp in data[key]["details_title"]:
          print("\033[1;32;40m- Frequency(in title):\033[0;0m\t {}".format(data[key]["details_title"][inp][0]))
          print("\033[1;32;40m- Indices:\033[0;0m\t {}".format(data[key]["details_title"][inp][1]))
          count += data[key]["details_title"][inp][0]
          indices = data[key]["details_title"][inp][1]
          title = list(filter(None, [ x.lower() for x in re.sub(r'\W+', ' ',data[key]["title"]).split(" ")])) if "title" in data[key] else []
          temp_title = []
          if is_stopwords:
            temp_title = [x for x in title if x not in stop_words] if not is_stem else [ps.stem(x) for x in title if x not in stop_words]
          else:
            temp_title = title if not is_stem else [ps.stem(x) for x in title]
          for i in indices:
            temp_title[i] = "\033[1;32;40m " + temp_title[i] + " \033[0;0m"
          temp_title_str = " ".join(temp_title)
          print("{}".format(temp_title_str))
        else:
          print("\033[1;32;40m ---Found none in title--- \033[0;0m")
        is_found =True
    if "abstract" in data[key]:  
      if inp in data[key]["abstract"]:    
        if inp in data[key]["details_abstract"]:
          if not ("title" in data[key] and inp in data[key]["title"]):
            print("\033[1;32;40m- ID:\033[0;0m\t {}".format(data[key]["id"]))
            if "title" in data[key]:
              print("\033[1;32;40m- Title:\033[0;0m\t {}".format(data[key]["title"]))
          print("\033[1;32;40m- Frequency(in abstract):\033[0;0m\t {}".format(data[key]["details_abstract"][inp][0]))
          print("\033[1;32;40m- Indices:\033[0;0m\t {}".format(data[key]["details_abstract"][inp][1]))
          count += data[key]["details_abstract"][inp][0]
          indices = data[key]["details_abstract"][inp][1]
          abstract = list(filter(None, [ x.lower() for x in re.sub(r'\W+', ' ',data[key]["abstract"]).split(" ")])) if "abstract" in data[key] else []
          temp_abstract = []
          if is_stopwords:
            temp_abstract = [x for x in abstract if x not in stop_words] if not is_stem else [ps.stem(x) for x in abstract if x not in stop_words]
          else:
            temp_abstract = abstract if not is_stem else [ps.stem(x) for x in abstract]
          for i in indices:
            temp_abstract[i] = "\033[1;32;40m" + temp_abstract[i] + "\033[0;0m"
          temp_abstract_str = " ".join(temp_abstract)
          print("{}".format(temp_abstract_str))
        else:
          print("\033[1;32;40m ---Found none in abstract--- \033[0;0m")
        is_found =True
    if is_found:
      print("\033[1;32;40m- Total counted:\033[0;0m\t {}".format(count))
      print("\033[1;32;40m ======================= \033[0;0m")

doc_list = load_file("posting.json")
dict_list = load_file("dictionary.json")
print("\033[1;32;40m ================================== \033[0;0m")
print("\033[1;32;40m ............ Starting ............ \033[0;0m")

while(term != "ZZEND"):
  inp = input("Enter a single query: ")
  term = inp
  u_input = ""
  if is_stem:
    ps = PorterStemmer()
    u_input = ps.stem(inp)
  else:
    u_input = inp
  if u_input in dict_list:
    get_data(doc_list,u_input)
  else:
    print("\033[38;2;255;0;0mNot Found, try another Query!\033[38;2;255;255;255m")

print("\033[1;32;40m ............ Ending ............ \033[0;0m")
print("\033[1;32;40m ================================== \033[0;0m")