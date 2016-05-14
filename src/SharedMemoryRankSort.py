
from multiprocessing.sharedctypes import Value, Array
from multiprocessing.context import Process
# function to sort
def debug(A, B, index, blocks, ranges, offset, rank):
    local_start = index * blocks
    with rank.get_lock():
        for start in range(ranges):
            for j in range(len(B)):
                if(B[j] < A[start + local_start]):
                    rank[start + local_start] = rank[start + local_start] + 1
                else:
                    break

    with offset.get_lock():
        for start in range(blocks):
            for pos in range(rank[start + local_start], len(offset)):
                offset[pos] += 1

    # debug rank
    for temp in range (len(rank)):
        print(rank[temp], end = " ")
    print()

    '''
    with offset.get_lock():
        for start in range(blocks):
            for pos in range(rank[start + local_start], len(offset)):
                offset[pos] += 1
    '''
    '''
    for temp in range (len(offset)):
        print(offset[temp], end = " ")
    print()
    '''







# main program
if __name__ == '__main__':
    # get input
    #n = int(input("Enter number of nodes: "))
    n = 2
    # test arrays
    A = Array('i',[2, 15, 17, 29, 35])
    B = Array('i', [1, 3, 6, 8, 9, 12, 16, 18, 22, 25, 30, 32, 36, 40])
    # offset array
    offset = Array('i', len(B))
    # rank array
    rank = Array('i', len(A))
    # get size of each block to work with
    block = [(int)(len(A) / n)] * n
    # get un even remainder
    remainer = (len(A) % n)
    # array to hold the range of elements needed to loop
    # this is only for the fact we can get odd sized arrays
    ranges = []
    # append the blocks to as ranges
    # since each block is how many values each cpu has
    for i in range(len(block)):
        ranges.append(block[i])
    # the last range element will contain the remainder
    ranges[len(ranges) - 1] = ranges[len(ranges) - 1] + remainer
    # create each process
    p = []
    for i in range (n):
        p.append(Process(target=debug, args=(A, B, i, block[i], ranges[i], offset, rank)).start())










