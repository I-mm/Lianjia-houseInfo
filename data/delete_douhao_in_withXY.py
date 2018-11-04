# coding=utf-8

DBcsvName = 'houseinfo_readable_withXY'

with open(DBcsvName + '.csv', 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    print(lines[0])

with open(DBcsvName + '_correct.csv', 'w', encoding='UTF-8') as fw:
    fw.write(
        "houseID" + "," + "title" + "," + "link" + "," + "community" + "," + "years" + "," + "housetype" + "," + "square" + "," + "direction" + "," + "floor" + "," + "taxtype" + "," + "totalPrice" + "," + "unitPrice" + "," + "followInfo" + "," + "decoration" + "," + "validdate" + "," + "coor_x,y")
    fw.write('\n')
    i = 1
    for line in lines:
        if i > 12000:
            exit(-1)
        if line.count(',') == 16:
            fw.write(line.strip() + '\n')
            print("count: " + str(i))
        i = i + 1
