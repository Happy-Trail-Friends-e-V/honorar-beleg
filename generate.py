#!/usr/bin/env python3

import csv
import argparse
import shutil
from pathlib import Path
import os

parser = argparse.ArgumentParser()
parser.add_argument("file", help="Input file")
parser.add_argument("-v", "--verbosity", action="count", help="Increase output verbosity")
args = parser.parse_args()

headrow = 0
count = 0

with open(args.file, newline='\n') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')
   
    for row in reader:
        # check, if you are in the header row. If yes, skip it.
        if headrow == 0:
            headrow += 1
            
        # go for each row
        # row[0] -> date
        # row[1] -> ip
        # row[2] -> name
        # row[3] -> id
        # row[4] -> type of training
        # row[5] -> date of training
        # row[6] -> duration in hours
        # row[7] -> amount of people trained
        # row[8] -> wants money
        # row[9] -> doesnt want money
        # row[10] -> this session is already covered by the organisation
        # row[11] -> privacy agreement
        
        # prepare rows
        date = row[0]
        ip = row[1]
        name = "".join(row[2].strip()).replace(" ", "")
        id = row[3]
        type = row[4]
        date_training = row[5]
        duration = row[6]
        amount_of_people = row[7]
        
        if row[8] == "Ja":
            wants_money = "Ja"
        else:
            wants_money = "Nein"
            
        if row[9] == "Ja":
            doesnt_want_money = "Ja"
        else:
            doesnt_want_money = "Nein"
            
        if row[10] == "Ja":
            covered = "Ja"
        else:
            covered = "Nein"
            
        if row[11] == "Ja":
            privacy = "Ja"
        else:
            privacy = "Nein"
            
        # copy template
        shutil.copyfile("src/beleg.md", "src/" + name + ".md")
        
        # replace the placeholders
        file = Path("src/" + name + ".md")
        file.write_text(file.read_text().replace('{{NAME}}', name))
        file.write_text(file.read_text().replace('{{ID}}', id))
        file.write_text(file.read_text().replace('{{TYPE}}', type))
        file.write_text(file.read_text().replace('{{DATE_TRAINING}}', date_training))
        file.write_text(file.read_text().replace('{{DURATION}}', duration))
        file.write_text(file.read_text().replace('{{AMOUNT_OF_PEOPLE}}', amount_of_people))
        file.write_text(file.read_text().replace('{{WANTS_MONEY}}', wants_money))
        file.write_text(file.read_text().replace('{{DOESNT_WANT_MONEY}}', doesnt_want_money))
        file.write_text(file.read_text().replace('{{COVERED}}', covered))
        file.write_text(file.read_text().replace('{{PRIVACY}}', privacy))
        
        # generate a pdf
        cmd = "pandoc src/" + name + ".md -o output/" + date_training + "_" + name + "_" + str(count) + ".pdf --from markdown+yaml_metadata_block+raw_html --template eisvogel --highlight-style breezedark"
        if headrow != 0:
            os.system(cmd)
        
        # delete the copied template
        os.remove("src/" + name + ".md")
        
        count += 1