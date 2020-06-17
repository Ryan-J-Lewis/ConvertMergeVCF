from pyliftover import LiftOver
import gzip
import sys

if len(sys.argv) < 3:
    print("Usage:\npython ConvertMergeHg19toHg38.py <hg19 input.vcf.gz> <hg38 input.vcf.gz> <output.vcf>")
    sys.exit()

hg19 = sys.argv[1]
hg38 = sys.argv[2]
out = sys.argv[3]

file1 = gzip.open(hg19, "r")

lo = LiftOver('hg19', 'hg38')

count = 0

samples1 = ""
samples2 = ""

positions = []

hold = open("hold", "w")
for line in file1:

    line = line.decode('utf8')

    if line[:2] != "##":
        if line[:1] != "#":
            data = line[:20]
            data = data.split("\t")
            chrom = "chr" + data[0]
            pos = int(data[1])
            converted = lo.convert_coordinate(chrom, pos)
            if converted != []:
                newPos = converted[0][1]
                hap = line.split("\t")
                a = hap[3]
                b = hap[4]
                for x in range(0,9):
                    del hap[0]
                hap = '\t'.join(hap)
                hold.write(str(newPos) + "\t"+ a + "\t"+ b + "\t" + hap)
                positions.append(newPos)
        else:
            samples1 = line

    count = count + 1
    sys.stdout.flush()
    sys.stdout.write('{0}\r'.format(count))

print("Hg19 to Hg38 done")

file1.close()
hold.close()

file2 = gzip.open(hg38, "r")
hold2 = open("hold2", "w")

count = 0
header = []
positions2 = []

for line in file2:

    line = line.decode('utf8')

    if line[:2] != "##":
        if line[:1] != "#":
            data = line[:50]
            data = data.split("\t")
            if int(data[1]) in positions:
                if int(data[1]) not in positions2:
                    hold2.write(line)
                    positions2.append(int(data[1]))
        else:
            samples2 = line
    else:
        header.append(line)
    count = count + 1
    sys.stdout.flush()
    sys.stdout.write('{0}\r'.format(count))

file2.close()
hold2.close()

print("Intersection done")

import linecache

hold3 = open("hold3", "w")

nums = list(range(len(positions)))
count = 0
for x in range(len(positions2)):
    for y in nums:
        line = linecache.getline('hold', y + 1)
        data = line[:20]
        data = data.split("\t")
        if int(data[0]) == positions2[x]:
            line = line.split("\t")
            del line[0]
            line = '\t'.join(line)
            hold3.write(line)
            nums.remove(y)
            continue
    count = count + 1
    sys.stdout.flush()
    sys.stdout.write('{0}\r'.format(count))
hold3.close()

print("ReOrder done")

out = open(out, "w")

for line in header:
    out.write(line)

data = samples1.split("\t")
for x in range(0,9):
    del data[0]

samples1 = '\t'.join(data)
samples = samples2[:-1] + "\t" + samples1
out.write(samples)

print("Writing File")

count = 0
with open("hold2") as hold2, open("hold3") as hold3:
    for line1, line2 in zip(hold2, hold3):
        x = line1[:50].split("\t")
        y = line2.split("\t")
        a2 = x[3]
        b2 = x[4]
        a1 = y[0]
        b1 = y[1]
        if a1 == a2 or b1 == b2:
            for z in range(0,2):
                del y[0]
            line = '\t'.join(y)
            line = line1[:-1] + "\t" + line
            out.write(line)
        elif a1 == b2 or b1 == a2:
            for z in range(0,2):
                del y[0]
            for z in range(0,len(y)):
                if y[z] == "1|1":
                    y[z] = "0|0"
                elif y[z] == "1|0":
                    y[z] = "0|1"
                elif y[z] == "0|1":
                    y[z] = "1|0"
                elif y[z] == "0|0":
                    y[z] = "1|1"
            line = '\t'.join(y)
            line = line1[:-1] + "\t" + line
            out.write(line)
        sys.stdout.flush()
        sys.stdout.write('{0}\r'.format(count))
        count = count + 1

out.close()
hold2.close()
hold3.close()
