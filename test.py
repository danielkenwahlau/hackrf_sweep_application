import csv
import argparse
#parse arguements
parser = argparse.ArgumentParser(description='Plots Hackrf Sweep Singleshot')
parser.add_argument('bin', type=int, nargs=1, help='the number of bins used for the sweep')
args = parser.parse_args()

print(args.bin[0])

print(type(args.bin[0]))

offset = 3
test = [1,2,3,4,5,6]

print(len(test))

test.insert(len(test)-offset,100)
print(test)


sweepcsv = open('sweep.csv')

sweepcsvReader = csv.reader(sweepcsv)

counter = 0

print('first 3')
for row in sweepcsvReader:
    print(','.join(row))
    if counter == 2:
        break
    counter +=1

print('last')
for row in sweepcsvReader:
    print(','.join(row))
