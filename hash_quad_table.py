# Name:        Tyler Davis
# Course:      CPE 202
# Instructor:  Dave Parkinson
# Assignment:  Project 4
# Term:        Fall 2017

class HashTableQuadPr:

    def __init__(self, capacity = 251):
        self.table = [None for _ in range(capacity)]
        self.num_items = 0
        self.step = 1

    def get_tablesize(self):
        return len(self.table)

    def __len__(self):
        return self.get_tablesize()

    def find(self, word):
        idx = self.myhash(word)
        i = 1
        while self.table[idx]:
            if self.table[idx][0] == word:
                return True
            idx = (idx + i ** 2 - (i - 1) ** 2) % len(self)
            i += 1
        return False      

    def read_stop(self, filename):
        stop_file = open(filename, "r")
        for word in stop_file:
            word = word.strip()
            self[word] = None
        stop_file.close()

    def read_file(self, filename, stop_table):
        read_file = open(filename, "r")
        line_num = 1
        for line in read_file:
            line = self.remove_punctuation(line.strip())
            for word in line.split(" "):
                word = word.lower()
                if word and word not in stop_table:
                    self[word] = line_num
            line_num += 1
        read_file.close()

    def __contains__(self, key):
        return self.find(key)  

    def remove_punctuation(self, text):
        new_text = ""
        for char in text:
            if char in " -":
                new_text += " "
            elif char.isalpha():
                new_text += char
        return new_text

    def save_concordance(self, outputfilename):
        filtered = [entry for entry in self.table if entry]
        alphabetical = self.sort(filtered)
        out_file = open(outputfilename, "w")
        for idx in range(len(alphabetical)):
            out_file.write(alphabetical[idx][0] + ":\t")
            for line_num_idx in range(len(alphabetical[idx][1])):
                out_file.write(str(alphabetical[idx][1][line_num_idx]))
                if line_num_idx < len(alphabetical[idx][1]) - 1:
                    out_file.write(" ")
            if idx < len(alphabetical) - 1:
                out_file.write("\n")
        out_file.close()

    def sort(self, tlist, place = 0):
        buckets = [[] for _ in range(27)]
        done = True
        for entry in tlist:
            if place <= len(entry[0]) - 1:
                done = False
                buckets[ord(entry[0][place]) - ord("a") + 1].append(entry)
            else:
                buckets[0].append(entry)
        tlist = []
        for bucket in buckets:
            if bucket:
                if done:
                    tlist += bucket
                else:
                    tlist += self.sort(bucket, place + 1)
        return tlist

    def get_load_factor(self):
        return self.num_items / len(self)

    def myhash(self, key, table_size = None):
        if not table_size:
            table_size = len(self)
        h = 0
        n = min(8, len(key))
        for idx in range(n):
            h = (31 * h) + ord(key[idx])
            h %= table_size
        return h

    def insert(self, word, line):
        idx = self.myhash(word)
        i = 1
        while self.table[idx]:
            if self.table[idx][0] == word:
                self.table[idx][1].append(line)
                return
            idx = (idx + i ** 2 - (i - 1) ** 2) % len(self)
            i += 1
        self.num_items += 1
        if self.get_load_factor() > 0.5:
            self.grow_table()
            self[word] = line
        else:
            self.table[idx] = (word, [line])

    def __setitem__(self, key, data):
        self.insert(key, data)

    def grow_table(self):
        new_table = [None for _ in range(2 * len(self) + 1)] 
        for entry in self.table:
            if entry:
                idx = self.myhash(entry[0], len(new_table))
                i = 1
                while new_table[idx]:
                    idx = (idx + i ** 2 - (i - 1) ** 2) % len(new_table)
                    i += 1
                new_table[idx] = entry
        self.table = new_table
