import threading

class Documents:
    def __init__(self):
        self.dictionary = {}
        self.posting = {}
        self.lookup = {}
        self._lock = threading.Lock()

    def update(self, id: str, title: str, words: list):
        with self._lock:
            doc_dictionary = {
                id: id,
                title: title
            }
            temp_word_dict = {}
            words_pool = set()
            
            for word in words:
                self.dictionary[word] = 1 if word not in self.dictionary else self.dictionary[word] + 1
                self.lookup[word] = [id] if word not in self.lookup else self.lookup[word] + [id]
                temp_word_dict[word] = 1 if word not in temp_word_dict else temp_word_dict[word] + 1
                words_pool.add(word)
                
            doc_dictionary['word_count'] = temp_word_dict
            doc_dictionary['words_pool'] = list(words_pool)
            
            
                
