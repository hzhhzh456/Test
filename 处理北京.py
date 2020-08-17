import csv

with open('北京数据1.csv','r',encoding='ANSI',newline='') as f:
    with open('new_data.csv','w',newline='')as csv_out_file:
        filereader = csv.reader(f)
        filewriter = csv.writer(csv_out_file)
        header = next(filereader)
        header_new = ['城市','区','方位','小区名','大小','租赁方式','朝向','月租','计费方式','几室','几厅','几卫','入住租期','看房','所在楼层','总楼层','电梯','车位','用水','用电','燃气','采暖']
        filewriter.writerow(header_new)
        for row in filereader:
            row[5] = row[5][:-1] #去除m2
            row[7] = row[7][0] #保存第一个字
            row[8] = row[8].replace('元/月', '')
            row[10] = row[10].replace('室', '')
            row[11] = row[11].replace('厅', '')
            row[12] = row[12].replace('卫', '')
            if row[13] != '随时入住':
                row[13] = row[13].replace('/', '')
            row[17] = row[17].replace('层', '')
            if row[16] != '高楼层' and row[16] != '中楼层' and row[16] != '低楼层':
                if int(row[16])<= int(row[17])/3:
                    row[16] = '低楼层'
                elif int(row[17])/3 < int(row[16]) <int(row[17])/3*2:
                    row[16] = '中楼层'
                else:
                    row[16] = '低楼层'
            row.pop(0)#去除编码格式
            filewriter.writerow(row)


