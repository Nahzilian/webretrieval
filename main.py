import shutil
from modules.preprocess import text_cleaner
import json
import gzip
# import threading
import logging
from modules.data import Documents
import multiprocessing as mp
# import concurrent
# import mmap
# import pandas as pd

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

docs = Documents()


# Worker process


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


def worker(line: str):
    obj: dict = json.loads(line)
    id = obj.get('id')
    title = obj.get('title')
    contents = obj.get('contents')
    logging.info(f"Executing update. ID: {id}")
    cleaned_contents = text_cleaner(contents)
    docs.update(id, title, cleaned_contents)
    logging.info(f"Executing finished. ID: {id}")
    # return {
    #     "id": id,
    #     "title": title,
    #     "contents": cleaned_contents
    # }
    return 'OK'


def get_result(result):
    logging.info(result)


def read_file(filepath: str):
    """
    Accepting GZIP filepath to retrieve information

    Args:
        filepath (str): _description_
    """

    with gzip.open(filepath, 'rt') as f:
        # temp = gzip.decompress(f)
        # json.dump(temp, 'temp.json')

        pool = mp.Pool(10)
        result = []
        for line in f:
            r = pool.apply_async(worker, args=[line], callback=get_result)
            result.append(r)

        for r in result:
            r.wait()


def main():
    logging.info("Started")
    # read_file('trec_corpus_5000.jsonl.gz')
    with gzip.open('trec_corpus_5000.jsonl.gz', 'rb') as f_in:
        with open('temp.json', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    logging.info('Finished')


if __name__ == "__main__":
    main()
