from multiprocessing.sharedctypes import Value, Array
from multiprocessing.context import Process

# function to sort
def rank_sort(A, B, index, blocks, ranges, new_blocks, new_ranges, offset, rank, result):
    # build rank
    build_rank(A, B, index, blocks, ranges, rank)
    # build offset
    build_offset(index, blocks, ranges, offset, rank)
    # combine A with result
    combine_A(A, index, rank, blocks, ranges, result)
    # combine B with result
    combine_B(B, index, offset, new_blocks, new_ranges, result)

# build up the rank
def build_rank(A, B, index, blocks, ranges, rank):
    # this gets the block size and uses the local var
    # as an offset
    local_start = index * blocks
    # lock the rank array just in case
    with rank.get_lock():
        # loop the range for each process
        for start in range(ranges):
            # loop the b array and do calculation
            for j in range(len(B)):
                # if b element is less then a array
                if(B[j] < A[start + local_start]):
                    # increment count at rank array at that element
                    rank[start + local_start] = rank[start + local_start] + 1
                else:
                    # when elements are no longer less than, no need to continue
                    break

# build the offset
def build_offset(index, blocks, ranges, offset, rank):
    # this gets the block size and uses the local var
    # as an offset
    local_start = index * blocks
    # lock offset array
    with offset.get_lock():
        # loop the number of blocks per process
        for start in range(ranges):
            # get that element with its offset (start, end)
            for pos in range(rank[start + local_start], len(offset)):
                # increment offset
                offset[pos] += 1

# compute A array to result array
def combine_A(A, index, rank, blocks, ranges, result):
    local_start = index * blocks
    # loop the range for each process
    with result.get_lock():
        # loop ranges of A per process
        for start in range(ranges):
            # algorithm
            pos = (start + local_start) + rank[start + local_start]
            result[pos] = A[start + local_start]

# computer B array to result array
def combine_B(B, index, offset, blocks, ranges, result):
    local_start = index * blocks
    # loop the range for each process
    with result.get_lock():
        # loop ranges of B per process
        for start in range(ranges):
            # algorithm
            pos = (start + local_start) + offset[start + local_start]
            result[pos] = B[start + local_start]

# main program
if __name__ == '__main__':
    # get input
    n = int(input("Enter number of nodes: "))
    # test arrays
    A = Array('i',[2, 15, 17, 29, 35])
    B = Array('i', [1, 3, 6, 8, 9, 12, 16, 18, 22, 25, 30, 32, 36, 40])
    # offset array
    offset = Array('i', len(B))
    # rank array
    rank = Array('i', len(A))
    # create result array
    result = Array('i', (len(A) + len(B)))
    # ***********************THIS IS FOR A ARRAY*****************************
    # get size of each block to work with
    block = [(int)(len(A) / n)] * n
    # get un even remainder
    remainder = (len(A) % n)
    # array to hold the range of elements needed to loop
    # this is only for the fact we can get odd sized arrays
    ranges = []
    # append the blocks to as ranges
    # since each block is how many values each cpu has
    for i in range(len(block)):
        ranges.append(block[i])
    # the last range element will contain the remainder
    ranges[len(ranges) - 1] = ranges[len(ranges) - 1] + remainder
    # ******************************** THIS IS FOR B ARRAY*********************
    # get size of each block to work with
    new_block = [(int)(len(B) / n)] * n
    # get un even remainder
    remainder = (len(B) % n)
    # array to hold the range of elements needed to loop
    # this is only for the fact we can get odd sized arrays
    new_ranges = []
    # append the blocks to as ranges
    # since each block is how many values each cpu has
    for i in range(len(new_block)):
        new_ranges.append(new_block[i])
    # the last range element will contain the remainder
    new_ranges[len(new_ranges) - 1] = new_ranges[len(new_ranges) - 1] + remainder
    # create process array
    p = []
    # create and set each process
    for i in range (n):
        p.append(Process(target=rank_sort,args=(A, B, i, block[i], ranges[i], new_block[i], new_ranges[i], offset, rank, result)))


    '''
    # start each process
    for i in range(n):
        p[i].start()
    #join each process
    for i in range(n):
        p[i].join()
    #display final results
    print("Results")
    for i in range(len(result)):
        print(result[i], end=" ")
    print()
'''


