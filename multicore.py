import pickle
from scoredgst import token_comparison
import time
import math
from multiprocessing import Process, Semaphore, Pool, Array
import copy

# comparing function

def cosine_dic(dic1,dic2):
    numerator = 0
    dena = 0
    for key1,val1 in dic1.iteritems():
        numerator += val1*dic2.get(key1,0.0)
        dena += val1*val1
    denb = 0
    for val2 in dic2.values():
        denb += val2*val2
    return numerator/math.sqrt(dena*denb)

"""Multiprocessing"""

# mutexes

mutex = Semaphore(1)
mutexPickle = Semaphore(1)

# reading datasets

with open('documents_gst_pickle.dictionary', 'rb') as documents_pickle:
    codes = pickle.load(documents_pickle)

# mapping codes to dict with { id: content }

codes_id = {}

for index, code in enumerate(codes):
    codes_id[index] = codes[code]

# preparing shared array, the integer is count of documents in the dataset 

uncompared = Array('i', 30)

# marking all documents as uncompared (because we could use only integers, 40 is used)

for ind, code in enumerate(codes_id):
    uncompared[ind] = code

def comparison(uncompared):
    global codes_id
    first = -1
    should_continue = True # are some uncompared documents?

    while should_continue:
        # find uncompared document
        with mutex:
            for index in range(0,30):
                if uncompared[index] < 40 and first == -1: # najdeme prvni nejmensi cislo
                    first = copy.copy(uncompared[index])
            uncompared[first] = 40
            print(first)

        if first != -1: # uncompared document found
            for second in codes_id:
                if second > first: # porovnáme s dokumenty pouze s vyšším id (nebyly porovnané ještě)
                    print(str(first) + ' >> ' + str(second))
                    t0 = time.time()
                    result = token_comparison(codes_id[first], codes_id[second], 3, threshold=0.3,
                                              compare_function=cosine_dic)
                    t1 = time.time()
                    print(t1 - t0)
                    with mutexPickle:
                        with open('documents_gst_results03_pickle.dictionary', 'a+') as documents_pickle:
                            pickle.dump({str(first) + '||' + str(second): result}, documents_pickle)
        else: # no uncompared document left
            should_continue = False
        first = -1

if __name__ == "__main__":
    process1 = Process(target=comparison, args=[uncompared])
    process2 = Process(target=comparison, args=[uncompared])
    process3 = Process(target=comparison, args=[uncompared])

    process1.start()
    process2.start()
    process3.start()
    process1.join()
    process2.join()
    process3.join()
