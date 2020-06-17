from pyliftover import LiftOver
import gzip
import sys

if len(sys.argv) < 2:
    print("Usage: \npython ConvertHg19toHg38.py <hg19 input.vcf.gz> <hg38 output.vcf>")

file = sys.argv[1]
out = sys.argv[2]

file = gzip.open(file, "r")
out = open(out, "w")

lo = LiftOver('hg19', 'hg38')
position = []
for line in file:
    line = line.decode('utf8')
    if line[:1] != "#":
        data = line.split("\t")
        chrom = data[0]
        pos = int(data[1])
        converted = lo.convert_coordinate(chrom, pos)
        if converted != [] and converted != None:
            newChrom = str(converted[0][0])
            newPos = str(converted[0][1])
            position.append(newPos)
            data[0] = newChrom
            data[1] = newPos
            data[2] = "."
            hold = '\t'.join(data)
            out.write(hold)
    else:
        out.write(line)
file.close()
out.close()
