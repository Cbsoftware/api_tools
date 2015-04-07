import json
import sys
import os

fin = open(sys.argv[1], 'r')
fout = open(os.path.join(sys.argv[2], os.path.basename(sys.argv[1])), 'w')

keep = sys.argv[3:len(sys.argv)]

print "reading data"

data = json.loads(fin.read())
fin.close()

smaller = []

for d in data[:10]:
    print str(d)

    small = {}

    for k in keep:
        small[k] = d[k]


    smaller.append(small)


print "writing data"

json.dump(smaller, fout)
fout.close()
