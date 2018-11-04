# coding=utf-8

DBcsvName = 'houseinfo'

with open(DBcsvName + '.csv', 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    print(lines[0])

with open(DBcsvName + '_readable.csv', 'a', encoding='UTF-8') as fw:
    if DBcsvName == 'community':
        fw.write(
            "id,title,link,district,bizcircle,tagList,onsale,onrent,year,housetype,cost,service,company,building_num,house_num,price,validdate")  # for community
    elif DBcsvName == 'hisprice':
        fw.write("houseID,totalPrice,date")  # for hisprice
    elif DBcsvName == 'houseinfo':
        fw.write(
            "houseID" + "," + "title" + "," + "link" + "," + "community" + "," + "years" + "," + "housetype" + "," + "square" + "," + "direction" + "," + "floor" + "," + "taxtype" + "," + "totalPrice" + "," + "unitPrice" + "," + "followInfo" + "," + "decoration" + "," + "validdate")

    elif DBcsvName == "rentinfo":
        fw.write(
            "houseID,title,link,region,zone,meters,other,subway,decoration,heating,price,pricepre,updatedate")  # for rentinfo
    elif DBcsvName == "sellinfo":
        fw.write(
            "houseID,title,link,community,years,housetype,square,direction,floor,status,source,totalPrice,unitPrice,dealdate,updatedate")  # for sellinfo
    else:
        print("ERROR, check DBcsvName")
        exit(-1)

    fw.write('\n')
    i = 1
    for line in lines:
        if line.count(',') >= 1:
            continue
        line = line.strip('\n').split("|")  # 将单个数据分隔开存好
        for e in line:
            if e == line[0]:
                fw.write(e)
            else:
                fw.write(',' + e)
        fw.write('\n')
        print("count: " + str(i))
        i = i + 1
