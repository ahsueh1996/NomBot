
d = {'a':1, 'b': 2, 'c': 3}
def takeValue(kv):
    return kv[1]
print(sorted(d.items(), key=takeValue, reverse=True))
