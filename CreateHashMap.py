class CreateHashMap:
    def __init__(self, initial_capacity=20):
        self.index = [[] for _ in range(initial_capacity)]

    #insert new item into hash table
    def insert(self, key, item):
        bucket_index = hash(key) % len(self.index)
        bucket_list = self.index[bucket_index]

        #update key if its already in bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        #not found, insert at end of bucket
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    #lookup
    def lookup(self, key):
        bucket_index = hash(key) % len(self.index)
        bucket_list = self.index[bucket_index]
        for pair in bucket_list:
            if key == pair[0]:
                return pair[1] #return associated item
        return None # return none if key isnt found

    #remove
    def hash_remove(self, key):
        bucket_index = hash(key) % len(self.index)
        bucket_list = self.index[bucket_index]

        for pair in bucket_list:
            if pair[0] == key:
                bucket_list.remove(pair)
                return True
        return False
