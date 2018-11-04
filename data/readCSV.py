# coding=utf-8
import getCoordinate

DBcsvName = 'houseinfo'

with open(DBcsvName + '.csv', 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    print(lines[0])

with open(DBcsvName + '_readable.csv', 'a', encoding='UTF-8') as fw:
    fw.write(
        "houseID" + "," + "title" + "," + "link" + "," + "community" + "," + "years" + "," + "housetype" + "," + "square" + "," + "direction" + "," + "floor" + "," + "taxtype" + "," + "totalPrice" + "," + "unitPrice" + "," + "followInfo" + "," + "decoration" + "," + "validdate" + "," + "coor_x,y")
    fw.write('\n')
    i = 1
    for line in lines:
        line = line.strip('\n').split("|")  # 将单个数据分隔开存好
        addr = line[3]
        coor = getCoordinate.get_addrCoor(addr)
        line.append('\"' + coor + '\"')
        for e in line:
            if e == line[0]:
                fw.write(e)
            else:
                fw.write(',' + e)
        fw.write('\n')
        print("count: " + str(i))
        i = i + 1
