import sys
import re

left=[]
right=[]
for line in sys.stdin:
    tokes=line.split()
    left.append(int(tokes[0]))
    right.append(int(tokes[1]))

left=sorted(left)
right=sorted(right)
cnt=0
ri=0
score=0
for l in left:
    # they are sorted, so find the correct spot
    while ri < len(right) and right[ri] < l :
        ri+=1
    while ri < len(right) and right[ri] == l:
        cnt += 1
        ri+=1
    if cnt > 0:
        score += (cnt * l)

    cnt=0
    if ri == len(right):
        break

print(score)


