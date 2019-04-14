import pickle

with open('documents_gst_results_pickle.dictionary', 'rb') as documents_pickle:
    codes = pickle.load(documents_pickle)

first = set(())

for code in codes:
    arr = code.split('||')
    if len(arr) == 2:
        first.add(arr[1])

first = list(first)

header = ';'
for f in first:
    header += f + ';'

print(header)

for f in first:
    results = f + ';'
    for s in first:
        if f == s:
            results += '1;'
        else:
            results += str(codes[f + '||' + s]) + ';'
    print(results)

# multiprocessing reader - because there are more object in one pickle

def loadall(filename):
    with open(filename, "r") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break

codes = loadall("documents_gst_results03_pickle.dictionary")
for code in codes:
    print(code)