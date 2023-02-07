from kleio.stores import N5FSIndexStore

path = "/Users/zouinkhim/Desktop/tmp/data/fly/kleio/indexes"

store = N5FSIndexStore(path)
zyx = 'ch_1/194.8.4'
xyz = 'ch_1/4.8.194'
print(store[zyx])
print(store[xyz])
