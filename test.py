row = ["jsdkfsd", '12']
if '.' not in row[1]:
    if len(row[1]) == 2:
        row[1] = '.' + row[1]
    else:
        row[1] = row[1][0] + '.' + row[1][1:]


print(row[1])