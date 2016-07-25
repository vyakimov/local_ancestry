import sys
f = open(sys.argv[1], 'r')
allowed_alleles = set(["A", "C", "T", "G", "N"])
seen_markers = set()
for line in f:
    # spit out all the lines with comments
    if line.startswith("#"):
        print line.strip()
        continue
    split = line.split("\t")

    # make sure every marker only appears once
    if split[1] not in seen_markers:
        seen_markers.add(split[1])
    else:
        continue

    # remove lines containing I and D in the REF allele field
    if split[3].strip() not in allowed_alleles:
        continue

    # replace all . with N for missing alleles in ALT allele field
    if split[4].strip() == ".":
        split[4] = "N"

    # spit it all out
    print "\t".join(split).strip()
