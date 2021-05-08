import json
import csv
count = 0
with open('neos.csv','r') as infile:
    contents = csv.reader(infile)
    next(contents)
    print(next(contents)[3])
    for line in infile:
        if line != '\n':
            count +=1
    infile.close()
print(count)

with open('neos.csv','r') as infile:
    count=0
    count_dia =0
    contents = csv.reader(infile)
    next(contents)
    for line in infile:
        line = line.split(',')
        if line[4] == 'Apollo':
            print(line[15])
        if line[4] != '':
            count+=1
        if line[15] != '':
            count_dia += 1
    infile.close()
print(count)
print(count_dia)


with open('cad.json','r') as infile:
    contents = json.load(infile)
    print(contents['count'])
    data = contents.get('data')
    for element in data:
        #print(element)
        if element[0] == '2015 CL' and '2000-Jan-01' in element[3]:
            print(element[3])
            print(element [4])

        if element[0] == '2002 PB' and '2000' in element[3]:
            print(element[3])
            print(element[7])
infile.close()


