import sys
f = open(sys.argv[1], 'r')
allowed_alleles = set(["A","C","T","G","N"])
for line in f:
	if line.startswith("#"):
		print line
		continue
	split = line.split("\t")
	if split[3].strip() not in allowed_alleles:
		continue
	if split[4].strip() == ".":
		split[4] = "N"
	print "\t".join(split).strip()
