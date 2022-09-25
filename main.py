import linecache
import os
import sys
from cmath import atan
from multiprocessing import Manager, Process


# Book object
class Book:
    def __init__(self, id, name, author, edition, publication):
        self.id = id
        self.name = name.rstrip().lstrip()
        self.author = author.rstrip().lstrip()
        self.edition = edition
        self.publication = publication
  
    def print(self):
        print("Book: " + self.id + "\t" + self.name + "\t" + self.author + "\t" + self.edition + "\t" + self.publication)

# Author object
class Author:
    def __init__(self, name, title):
        self.name = name.rstrip().lstrip()
        self.titles = [title.rstrip().lstrip()]

    def __eq__(self, other):
        return self.name == other.rstrip().lstrip()

    def addTitle(self, title):
        title = title.rstrip().lstrip()
        # add title only if not already present
        if title not in self.titles:
            self.titles.append(title)
        return self

    def print(self):
        print("Author: " + self.name + "\t  %d " % len(self.titles))

def getLineCountFromFile(filename: str) -> int:
    with open(filename) as f:
        size=len([0 for _ in f])
    return size

def readLinesFromFile(books, authors, filename: str, offset: int, limit: int):
    for i in range(offset, offset+limit):
        line = linecache.getline(filename, i).split(";")
        # data structure to books
        books.append(Book(line[0],line[1],line[2],line[3],line[4]))
        # verify if authors exists on list
        if line[2] in authors:
            # if exists add title to object of author
            authors[authors.index(line[2])] = authors[authors.index(line[2])].addTitle(line[1])
        else:
            # if not exists add author and title to list
            authors.append(Author(line[2],line[1]))

def partition(number, n):
    width = number // n
    ret = [(int(1 + i*width), int(width) ) for i in range(n)]
    if number % n != 0:
        ret[-1] = (ret[-1][0],ret[-1][1]+1)        
    return ret

def main():    
    threads = []
    #validate args
    if ( len(sys.argv) != 3 ):
        print ('%s <filename> <num_threads>' % sys.argv[0])
        sys.exit(0)
    #get the file name and the number of threads
    filename = sys.argv[1]
    threadsnum = int(sys.argv[2])
    #get count lines from file
    lines = getLineCountFromFile(filename)
    #partition into blocks to threads  
    sections = partition(lines, threadsnum)
    #shared list to multiprocessing
    with Manager() as manager:
        books = manager.list() 
        authors = manager.list() 
        for s in sections:
            t = Process(
                target=readLinesFromFile, args=[books, authors, filename, s[0], s[1]])
            threads.append(t)        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        #TODO: needs finalization
        print ('list size: %d books' % len(books))
        print ('list size: %d authors' % len(authors))
        for a in authors:
            a.print()
        #Write author list into txt file
        if os.path.exists("authors.txt"):
            os.remove("authors.txt")
        with open(r'authors.txt', 'w') as fp:
            for i in authors:
                fp.write(i.name.ljust(45) + ";%d\n" % len(i.titles))
        
        

    #TODO: needs finalization
    # pi = 0	
    # for p in res:
    #     pi = pi + p
    # print ('PI: %.15f' % pi)

if __name__ == '__main__':
    main()
