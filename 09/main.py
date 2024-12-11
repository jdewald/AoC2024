import sys


FULL_ONLY = False
# only reason we're doing this is python can be an ass about giant single lines
f = open(sys.argv[1], 'r')
filemap = list(f.readline().strip())
f.close()
# the filemap is <filesize><freesize><filesize><freesize>...
#filemap = list(sys.stdin.readline().strip())

if len(sys.argv) > 2:
    FULL_ONLY = int(sys.argv[2]) == 1

size = len(filemap)

# thought, we can do this in a single pass from back to front and meet in the middle

total = 0
i = 0
z = size-1

f = 0
back = int((size - 1) / 2)

realpos = 0

need = int(filemap[z])
freeblocksize = 0
output = ''
# will definitely fill this space
free = 0
while True:
    if z <= i:
        break
    blocksize = int(filemap[i])
#    print(f"{f} is {blocksize}")
#    print((back, need, freeblocksize))
    # 5*4 + 6*4 + 7 * 4 = (5+6+7)*4 = 18 * 4
    # (5 + (5+3)) * (1.5) = (13 * 1.5)
    block_sum = f * ((realpos + ((blocksize-1)+realpos)) * (blocksize / 2))
#    print(f"{f} worth {block_sum}")
    output +=  (str(f) * blocksize)
#    print(output)
    total += block_sum
    realpos += blocksize

    f+=1 # go to next block
    # now grab a free block
    i+=1

    if i >= size:
        break
    if z < i:
        break

#    print(f"Need {need} for {back}")
    
    freeblocksize = int(filemap[i])
    i+=1
#    print(f"Have a {freeblocksize} free block at {realpos} ({i})")

    while freeblocksize > 0:

        usable = min(freeblocksize, need)
        block_sum = back * (realpos + ((usable-1)+realpos)) * (usable / 2)
        total += block_sum
        output += (str(back) * usable)
#        print(f"Added block {back} {usable} (worth {block_sum})")
        need -= usable
        realpos += usable
        freeblocksize -= usable

        if need == 0:
            # consume all of it
            z -= 2
            if z <i :
                break
            back -= 1
            need = int(filemap[z])
            filemap[z+1] = str(int(filemap[z+1]) + need)
#            print((back, need))

#        print(output)
print(output)
if need > 0:
    block_sum = back * (realpos + ((need-1)+realpos)) * (need / 2)
    total += block_sum

    # if we are here, then we're searching for a free block, which puts us back at the beginning 
print(total)

        







