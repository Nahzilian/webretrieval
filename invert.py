import nltk
from nltk.stem import PorterStemmer
import re
import json
import sys
from colorama import init, AnsiToWin32

init(wrap=False)
stream = AnsiToWin32(sys.stderr).stream
# For installation
# nltk.download()

def write_to_file(filename, a_list):
  with open(filename, 'w') as fp:
    json.dump(a_list, fp)

# Helper function to read and separate files based on special character (In this case, I'm using ".I" since every document section is formatted that way)

def get_file_data(filename, splitchar='\n'):
    data = list(
      filter(None, open(filename, "r").read().strip().split(splitchar)))
    return [x.replace("\t", " ").replace("\n", " ") for x in data]

def section_removal(data):
    filtered = []
    important_sections = [" .I", " .T", " .W", " .B", " .A"]
    for index in data:
        new_data = []
        temp = (" .I" + index.replace(".T", "REMOVE_HERE .T").replace(".W", "REMOVE_HERE .W").replace(".B", "REMOVE_HERE .B").replace(
            ".A", "REMOVE_HERE .A").replace(".N", "REMOVE_HERE .N").replace(".X", "REMOVE_HERE .X").replace(".K", "REMOVE_HERE .K").replace(".C", "REMOVE_HERE .C")).split("REMOVE_HERE")
        for index in temp:
            if index[:3] in important_sections:
                new_data.append(index)
        filtered.append(new_data)
    return filtered

def data_cleaner(data, is_stem, is_stopword):
    filtered_str = ""
    ps = PorterStemmer()
    important_sections = [" .I", " .T", " .W"," .A"]
    common_words = [x.lower() for x in get_file_data("common_words", "\n")]
    for index in data:
        temp_lst = (" .I" + index.replace(".T", "REMOVE_HERE .T").replace(".W", "REMOVE_HERE .W").replace(".B", "REMOVE_HERE .B").replace(
            ".A", "REMOVE_HERE .A").replace(".N", "REMOVE_HERE .N").replace(".X", "REMOVE_HERE .X").replace(".K", "REMOVE_HERE .K").replace(".C", "REMOVE_HERE .C")).split("REMOVE_HERE")
        temp_data = []
        for index in temp_lst:
            if index[:3] in important_sections:
                temp_data.append(index)
        filtered_str += ' '.join(temp_data)
    cleaned_str = re.sub('[^A-Za-z0-9]+', ' ', filtered_str).split(" ")
    lowered = [ps.stem(x.lower()) for x in cleaned_str if not x.isnumeric() and not x == ''] if is_stem else [
        x.lower() for x in cleaned_str if not x.isnumeric() and not x == '']
    no_num = [x for x in lowered if not bool(re.search(r'\d', x))]
    return [x for x in no_num if x not in common_words] if is_stopword else no_num

# Generate a separate dictionary for faster search

def dictionary_maker(data, is_stem, is_stopword,data_input):
  raw_words = data_cleaner(data_input, is_stem, is_stopword)
  word_list = sorted(set(raw_words))
  lookup_dict, dictionary = dict(), dict()
  for term in word_list:
    for key in data:
      if term in data[key]["words_pool"]:
        word_counter = dictionary[term] + 1 if term in dictionary else 1
        dictionary[term] = word_counter
        if term in lookup_dict:
          if not key in lookup_dict[term]:
            lookup_dict[term].append(key)
        else:
            lookup_dict[term] = [key]
  print("\033[1;32;40m.... Writing to file: dictionary ....\033[0;0m", file=stream)
  write_to_file("dictionary.json", dictionary)
  print("\033[1;32;40m.... Writing to file: lookup_dict ....\033[0;0m", file=stream)
  write_to_file("lookup.json", lookup_dict)

def posting_list(data_input):
  data = section_removal(data_input)
  all_dict = dict()
  for index in data:
    temp_dict = dict()
    for section in index:
      if section[:3] == " .I":
        temp_dict["id"] = section[3:].strip()
      if section[:3] == " .T":
        temp_dict["title"] = section[3:].strip()
      if section[:3] == " .W":
        temp_dict["abstract"] = section[3:].strip()
      if section[:3] == " .A":
        temp_dict["authors"] = section[3:].strip()
    all_dict[index[0][3:].strip()] = temp_dict
  return all_dict

def format_posting_list(data_input,is_stem,is_stopword):
  data = posting_list(data_input)
  stop_words = get_file_data("common_words"," ")[0].split(" ")
  ps = PorterStemmer()
  for key in data:
    title = list(filter(None, [ x.lower() for x in re.sub('[^A-Za-z0-9]+',' ',data[key]["title"]).split(" ") if not x.isnumeric()])) if "title" in data[key] else []
    abstract = list(filter(None,[ x.lower() for x in re.sub('[^A-Za-z0-9]+',' ',data[key]["abstract"]).split(" ") if not x.isnumeric()])) if "abstract" in data[key] else []
    author = [x.lower() for x in re.sub('[^A-Za-z0-9]+',' ', data[key]["authors"]).split(" ") if not x.isnumeric() and not x == ''] if "authors" in data[key] else []
    words_pool= sorted(set(list(filter(None,(" ".join(title) + " " + " ".join(abstract)).split(" ")))))
    temp_title = []
    temp_abstract = []
    temp_word_pools = []
    temp_author = []
    if is_stem:
      temp_title = [ps.stem(x) for x in title if x not in stop_words] if is_stopword else [ps.stem(x) for x in title]
      temp_abstract = [ps.stem(x) for x in abstract if x not in stop_words] if is_stopword else [ps.stem(x) for x in abstract]
      temp_word_pools = [ps.stem(x) for x in words_pool if x not in stop_words] if is_stopword else [ps.stem(x) for x in words_pool]
      temp_author = [ps.stem(x) for x in author if x not in stop_words] if is_stopword else [ps.stem(x) for x in author]
    else:
      temp_title = title if not is_stopword else [x for x in title if x not in stop_words]
      temp_abstract = abstract if not is_stopword else [x for x in abstract if x not in stop_words]
      temp_word_pools = words_pool if not is_stopword else [x for x in words_pool if x not in stop_words]
      temp_author = author if not is_stopword else [x for x in author if x not in stop_words]
    temp_word_pools += temp_author
    data[key]["words_pool"] = temp_word_pools
    data_title_dict = dict()
    data_abstract_dict = dict()
    unique_title = []
    unique_abstract = []
    for i in temp_title:
      if i not in unique_title:
        unique_title.append(i)
    for i in temp_abstract:
      if i not in unique_abstract:
        unique_abstract.append(i)
    unique_title.sort()
    unique_abstract.sort()
    for i in unique_title:
      indices = [index for index, x in enumerate(temp_title) if x == i]
      data_title_dict[i] = [temp_title.count(i),indices]
    for i in unique_abstract:
      indices = [index for index, x in enumerate(temp_abstract) if x == i]
      data_abstract_dict[i] = [temp_abstract.count(i),indices]
    temp_count = dict()
    for word in temp_word_pools:
      count = 0
      if word in data_abstract_dict:
        count += data_abstract_dict[word][0]
      elif word in data_title_dict:
        count += data_title_dict[word][0]
      else:
        count+=1
      temp_count[word] = count
    data[key]["word_count"] = temp_count
  print("\033[1;32;40m.... Writing to list: Posting ....\033[0;0m", file=stream)
  dictionary_maker(data,is_stem,is_stopword,data_input)
  write_to_file("posting.json",data)

def main(is_stem,is_stopword):
  print("\033[1;32;40m.... Stemming .... {}\033[0;0m".format(is_stem), file=stream)
  print("\033[1;32;40m.... Remove stop words .... {}\033[0;0m".format(is_stopword), file=stream)
  print("\033[1;32;40m.... Extracting file ....\033[0;0m", file=stream)
  data = get_file_data("cacm.all", ".I")
  format_posting_list(data,is_stem,is_stopword)


main(True,True)