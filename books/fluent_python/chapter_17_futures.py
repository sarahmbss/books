'''
    - Both types of Future have a .done() method that is nonblocking and returns a Boolean
    that tells you whether the callable linked to that future has executed or not. Instead of
    asking whether a future is done, client code usually asks to be notified
    - There is also a .result() method, which works the same in both classes when the future
    is done: it returns the result of the callable, or re-raises whatever exception might have
    been thrown when the callable was executed
    - Strictly speaking, the scripts don't run in parallel. The concurrent.futures examples are limited by the GIL, and later
    we will see that asyncio is single-threaded

    Blocking I/O and the GIL
        - The CPython interpreter is not thread-safe internally, so it has a Global Interpreter Lock
        (GIL), which allows only one thread at a time to execute Python bytecodes. That's why
        a single Python process usually cannot use multiple CPU cores at the same time.
        - This means Python programs that are I/O bound can
        benefit from using threads at the Python level: while one Python thread is waiting for
        a response from the network, the blocked I/O function releases the GIL so another thread can run
'''
# Example of code using futures to download flags concurrently
import os
import time
import sys
import requests
from concurrent import futures

MAX_WORKERS = 20

POP20_CC = ('CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'http://flupy.org/data/flags'
DEST_DIR = 'downloads/'

def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)

def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content

def show(text):
    print(text, end=' ')
    sys.stdout.flush()

def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc

def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, sorted(cc_list)) # it returns a generator that can be iterated over to retrieve the value returned by each function
    return len(list(res)) 

def main(download_many):
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))

if __name__ == '__main__':
    main(download_many)