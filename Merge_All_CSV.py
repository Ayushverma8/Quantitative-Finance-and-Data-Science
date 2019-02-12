from glob import glob

with open('main.csv', 'a') as singleFile:
    for csv in glob('*.csv'):
        if csv == 'main.csv':
            pass
        else:
            for line in open(csv, 'r'):
                singleFile.write(line)