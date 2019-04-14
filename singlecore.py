import pickle
from scoredgst import token_comparison
import time
import math

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

# loading dataset with files

with open('documents_gst_pickle.dictionary', 'rb') as documents_pickle:
    codes = pickle.load(documents_pickle)

results = {}
compared = []

for first in codes:
    print(first)
    for second in codes:
        if not second in compared:
            print('  ' + second)
            if first != second:
                t0 = time.time()
                result = token_comparison(codes[first], codes[second], 3, threshold=0.5, compare_function=cosine_dic)
                t1 = time.time()
                print(t1 - t0)

                results[ first + '||' + second] = result
    compared.append(first)

# saving results into a file

with open('documents_gst_results_pickle.dictionary', 'wb') as documents_pickle:
    pickle.dump(results, documents_pickle)