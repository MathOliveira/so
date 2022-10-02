import linecache
import os
import sys
from multiprocessing import Manager, Process


# Book object
class Book:
    def __init__(self, id, name, author, edition, publication):
        self.id = id
        self.name = name.rstrip().lstrip()
        self.author = author.rstrip().lstrip()
        self.edition = edition
        self.publications = [publication.rstrip().lstrip()]
    
    def __eq__(self, other):
        return self.name == other.rstrip().lstrip()   

    def addPublication(self, publication):
        publication = publication.rstrip().lstrip()
        # add publication only if not already present
        if publication not in self.publications:
            self.publications.append(publication)
        return self     
  
    def print(self):
        print("Book: " + self.id + "\t" + self.name + "\t" + self.author + "\t" + self.edition + "\t" + ','.join(self.publications))

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

# Author object
class Year:
    def __init__(self, year):
        self.year = year.rstrip().lstrip()
        self.quantity = 1

    def __eq__(self, other):
        return self.year == other.rstrip().lstrip()

    def incrementQuantity(self):
        self.quantity = self.quantity + 1
        return self

    def print(self):
        print("Year: " + self.year + "\t  %d " % self.quantity)          

def getLineCountFromFile(filename: str) -> int:
    with open(filename) as f:
        size=len([0 for _ in f])
    return size

def readLinesFromFile(books, authors, years, bestYear, filename: str, offset: int, limit: int):
    for i in range(offset, offset+limit):
        line = linecache.getline(filename, i).split(";")
        # data structure to books, authors and editors
        # verify if books exists on list
        bookTitle = line[1].rstrip().lstrip()
        if bookTitle in books:
            # if exists add publication to object of book
            books[books.index(bookTitle)] = books[books.index(bookTitle)].addPublication(line[4])
        else:
            # if not exists add book to list
            books.append(Book(line[0],bookTitle,line[2],line[3],line[4]))
        # verify if authors exists on list
        bookAuthor = line[2].rstrip().lstrip()
        if bookAuthor in authors:
            # if exists add title to object of author
            authors[authors.index(bookAuthor)] = authors[authors.index(bookAuthor)].addTitle(line[1])
        else:
            # if not exists add author to list
            authors.append(Author(bookAuthor,line[1]))
        # get publication year
        yearPublication = line[4].rstrip().lstrip()
        # initialize bestYear
        if len(bestYear) == 0:
                bestYear.append(Year(line[4].rstrip().lstrip()))
        # verify if year of publication exists on list
        if yearPublication in years:
            # if exists increment quantity of publications on the year
            years[years.index(yearPublication)] = years[years.index(yearPublication)].incrementQuantity()
            # verify if its the best year (biggest number of publications)
            if years[years.index(yearPublication)].quantity > bestYear[0].quantity:
                bestYear.pop()
                bestYear.append(years[years.index(yearPublication)])
        else:
            # if not exists add year to list
            years.append(Year(yearPublication))            

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
        years = manager.list() 
        bestYear = manager.list()
        for s in sections:
            t = Process(
                target=readLinesFromFile, args=[books, authors, years, bestYear, filename, s[0], s[1]])
            threads.append(t)        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        #Write author list into txt file
        if os.path.exists("authors.txt"):
            os.remove("authors.txt")
        with open(r'authors.txt', 'w') as fp:
            for a in authors:
                fp.write(a.name.ljust(45) + ";%d\n" % len(a.titles))
        #Write books list into txt file
        if os.path.exists("livro.txt"):
            os.remove("livro.txt")
        with open(r'livro.txt', 'w') as fp:
            for b in books:
                fp.write(b.name.ljust(45) + ";" + ','.join(b.publications) + ";\n")
        #Final resume
        print ('----------------------------------------------------------------')
        print ('FINAL RESUME\n')
        print ('Books:'.ljust(45) + '%d' % len(books))
        print ('Year with more books published:'.ljust(45) + bestYear[0].year)
        print ('Total of years that there were publications:'.ljust(45) + '%d' % len(years))
        print ('----------------------------------------------------------------')
        #TODO: remover trecho
        for a in years:
            a.print()
        
                
if __name__ == '__main__':
    main()
