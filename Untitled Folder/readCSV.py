# coding=utf-8
import getCoordinate

DBcsvName = 'houseinfo'

with open(DBcsvName + '.csv', 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    print(lines[0])

with open(DBcsvName + '.txt', 'w', encoding='UTF-8') as fw:
    i = 1
    for line in lines:
        line = line.split("|")  # 将单个数据分隔开存好
        addr = line[3]
        coor = getCoordinate.get_addrCoor(addr)
        line.append(coor)
        for e in line:
            fw.write(e + '\t')
        fw.write('\n')
        print("count: " + str(i))
        i = i + 1
