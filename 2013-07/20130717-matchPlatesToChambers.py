from __future__ import print_function
import sys
import re
import os
from csv import DictReader

def _get_plate_tray_pos_dict(platefile):
    plate_fh = open(platefile)
    plate = DictReader(plate_fh)
    plate_dict = {}
    for row in plate:
        row_letter = row[""]  # it's a hack, but "" is the name of the 1st col
        for iii in xrange(1,13):
            col_num = str(iii)
            sample = row[col_num]
            if len(sample) < 2:
                continue
            # tuple of (chamber, pos)
            #sys.stderr.write("%s %s\n" %( row_letter, col_num) )
            sample = (int(sample.split()[0]), sample.split()[1])
            sample_coord = row_letter + col_num
            plate_dict[sample_coord] = sample
    plate_fh.close()
    return plate_dict

with open(sys.argv[1]) as fh:
    lst = list(DictReader(fh))

samples = {
        "Col": [],
        "Ler": [],
        "Cvi": [],
        }

for dct in lst:
    samples[dct["geno"]].append((dct["plate"], dct["pos"]))

walk = os.walk("../2013-03/")
allfiles = []
for dp, dn, files in walk:
    allfiles.extend(files)

allfiles = filter(lambda fle: fle.find("harvestplate") >= 0, allfiles)
allfiles = filter(lambda fle: fle.find("genotype") < 0, allfiles)
csvs = ["../2013-03/" + x for x  in allfiles]


plates = {}
for csv in csvs:
    plate = re.search("(\\d+)\\.csv", csv).group(1)
    plates[plate] = csv

platedicts = {}
for plate, csv in plates.iteritems():
    platedicts[plate] = _get_plate_tray_pos_dict(csv)

print("Genotype,Plate,PlatePos,Chamber,TrayPos")
for geno, sample_list in samples.iteritems():
    for sample in sample_list:
        sam_plate, sam_pos = sample
        cond = platedicts[sam_plate][sam_pos]
        print("{geno},{sp},{ps},{cond[0]},{cond[1]}".format(
                geno=geno, sp=sam_plate, ps=sam_pos, cond=cond))
