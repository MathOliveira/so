import linecache
import multiprocessing
import sys


def getLineCountFromFile(filename: str) -> int:
    with open(filename) as f:
        size=len([0 for _ in f])
    return size

def readLinesFromFile(filename: str, offset: int, limit: int):
    #TODO: needs finalization
    for i in range(offset, offset+limit):
        author = linecache.getline(filename, i).split(";")[2]
        print(author)
        # print(str(offset))
    # fs = open(filename)
    # for offset, limit in enumerate(fs):
    # fs.close()
    # with open(filename) as infile:
    #     lines = infile.readlines()
    #     line = random.choice(lines).strip()
    #     tokens = line.split(':')
    #     return ' '.join(tokens)

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
    for s in sections:
        t = multiprocessing.Process(
			target=readLinesFromFile, args=[filename, s[0], s[1]])
        threads.append(t)        
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    #TODO: needs finalization
    # pi = 0	
    # for p in res:
    #     pi = pi + p
    # print ('PI: %.15f' % pi)
   

if __name__ == '__main__':
    main()
