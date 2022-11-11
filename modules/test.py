import logging
import multiprocessing as mp
import time
import random

# Worker process


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


def work(item, count):
    name = mp.current_process().name
    logging.info(f'{name} started: {item}')
    for x in range(count):
        logging.info(f'{name}: {item} = {x}')
        time.sleep(3)
    logging.info(f'{name} finished')
    return f"{item} is finished"

# Main process


def proc_result(result):
    logging.info(f'Result: {result}')


def main():
    logging.info("Started")

    max = 212651
    pool = mp.Pool(100) 
    result = []
    for x in range(max):
        item = 'Item' + str(x)
        count = random.randrange(1, 5)
        # pool.map could be used for our case, and with async, but for this case we use apply_async
        r = pool.apply_async(work, args=[
                             item, count], callback=proc_result)
        result.append(r)

    for r in result:
        r.wait()
        
    # pool.close or pool.termninate
    pool.close()
    pool.join()
    logging.info('Finished')

if __name__ == "__main__":
    main()
