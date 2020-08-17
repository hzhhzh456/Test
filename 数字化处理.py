# -*- coding: utf-8 -*
import re
import csv
#创建元素集
chengshi = set()
qu = set()
fangwei = set()
fangwuming = set()
zulinfangshi = set()
chaoxiang = set()
jifeifangshi = set()
ruzhu = set()
zuqi = set()
kanfang = set()
dianti = set()
chewei = set()
yongshui = set()
yongdian = set()
ranqi = set()
gongnuan = set()
#将对应信息写入元素集
with open('new_data.csv','r',newline='',encoding='utf-8')as f:
    data = f.read()
    list_a = data.split("\n")
    for i in range(1,1502):
        list_b = list_a[i].split(" ")
        chengshi.add(list_b[0])
        qu.add(list_b[2])
        fangwei.add(list_b[3])
        fangwuming.add(list_b[4])
        zulinfangshi.add(list_b[6])
        chaoxiang.add(list_b[7])
        jifeifangshi.add(list_b[9])
        ruzhu.add(list_b[13])
        zuqi.add(list_b[14])
        kanfang.add(list_b[15])
        dianti.add(list_b[18])
        chewei.add(list_b[19])
        yongshui.add(list_b[20])
        yongdian.add(list_b[21])
        ranqi.add(list_b[22])
        gongnuan.add(list_b[23])
#楼层
dict_louceng = {}
dict_louceng["低楼层"]=1
dict_louceng["中楼层"]=2
dict_louceng["高楼层"]=3
#区
dict_qu = {}
for i in range(len(qu)):
    dict_qu[list(qu)[i]] = i + 1#给区编号，下同理
#方位
dict_fangwei = {}
for i in range(len(fangwei)):
    dict_fangwei[list(fangwei)[i]] = i + 1
#房屋名
dict_fangwuming = {}
for i in range(len(fangwuming)):
    dict_fangwuming[list(fangwuming)[i]] = i + 1
#租赁方式
dict_zulinfangshi = {}
dict_zulinfangshi["整租"] = 1
dict_zulinfangshi["合租"] = 2
#朝向
dict_chaoxiang = {}
dict_chaoxiang["东"] = 1
dict_chaoxiang["南"] = 2
dict_chaoxiang["西"] = 3
dict_chaoxiang["北"] = 4
dict_chaoxiang["东北"] = 5
dict_chaoxiang["东南"] = 6
dict_chaoxiang["西北"] = 7
dict_chaoxiang["西南"] = 8
#计费方式
dict_jifeifangshi = {}
dict_jifeifangshi["月付价"] = 1
dict_jifeifangshi["季付价"] = 2
dict_jifeifangshi["半年付价"] = 3
dict_jifeifangshi["年付价"] = 4
dict_jifeifangshi["NULL"] = 5
#入住
dict_ruzhu = {}
dict_ruzhu["NULL"] = 0
for i in range(len(ruzhu)):
    if list(ruzhu)[i] == "随时入住":
        dict_ruzhu[list(ruzhu)[i]] = 2
    else:
        dict_ruzhu["具体入住"] = 1
#看房
dict_kanfang = {}
dict_kanfang["NULL"] = 0
dict_kanfang["随时可看"] = 1
dict_kanfang["需提前预约"] = 2
dict_kanfang["一般下班后可看"] = 3
#电梯
dict_dianti = {}
dict_dianti["NULL"] = 0
dict_dianti["无"] = 1
dict_dianti["有"] = 2
#用水
dict_yongshui = {}
dict_yongshui["NULL"] = 0
dict_yongshui["民水"] = 1
dict_yongshui["商水"] = 2
#车位
dict_chewei = {}
dict_chewei["NULL"] = 0
dict_chewei["免费使用"] = 1
dict_chewei["租用车位"] = 2
#用电
dict_yongdian = {}
dict_yongdian["NULL"] = 0
dict_yongdian["民电"] = 1
dict_yongdian["商电"] = 2
#燃气
dict_ranqi = {}
dict_ranqi["NULL"] = 0
dict_ranqi["无"] = 1
dict_ranqi["有"] = 2
#供暖
dict_gongnuan = {}
dict_gongnuan["NULL"] = 0
dict_gongnuan["集中供暖"] = 1
dict_gongnuan["自采暖"] = 2
with open("new_data.csv", "w")as f:
    f.write("城市 区 方位 房屋名 大小 租赁方式 朝向 月租 计费方式 几室 几厅 几卫 入住 租期 看房 所在楼层 总楼高 电梯 车位 用水 用电 燃气 供暖 \n")
    for i in range(1, 1501):
        list2 = list1[i].split(" ")
        f.write("3 "+str(dict_qu[list2[2]])+" "+str(dict_fangwei[list2[3]]) + " "+str(dict_fangwuming[list2[4]]) + " ")
        list2[6]=list2[6].replace('合租','2')
        list2[6] = list2[6].replace('整租', '1')
        f.write(str(list2[5]) + ' ' +str(list2[6])+' ')
        chaoxiang = re.findall("(.*?)/", list2[7])
        if chaoxiang:
            f.write(str(dict_chaoxiang[chaoxiang[0]])+" ")
        else:
            f.write(str(dict_chaoxiang[list2[7]])+" ")
        money = re.findall("(.*?)元/月", list2[8])
        if list2[9] == "NULL":
            f.write(money[0]+" 0 ")
        else:
            f.write(money[0]+" "+str(dict_jifeifangshi[list2[9]])+" ")
        size0 = re.findall("(.*)室", list2[10])#室
        size1 = re.findall("(.*)厅", list2[11])#卫
        size2 = re.findall("(.*)卫", list2[12])#厅
        if size0:#如果有室的信息
            f.write(size0[0]+" "+size1[0]+" "+size2[0]+" ")
        else :
            f.write("0 0 0 ")
        if list2[13]=="随时入住" or list2[13] == "NULL":
            ruzhu = list2[13]
        else:
            ruzhu = "具体入住"
        f.write(str(dict_ruzhu[ruzhu])+" ")
        tenancy_time = re.findall("(.)年", list2[14])#租期
        if tenancy_time:#如果是年X12变成月
            t_time = int(tenancy_time[0])*12
            f.write(str(t_time)+" ")  # 租期编号
        else:
            tenancy_time = re.findall("~(.*)个月", list2[14])
            if tenancy_time:
                f.write(str(tenancy_time[0])+" ")
            else:
                f.write("0 ")
        if list2[15]=="NULL":#看房的信息
            f.write("0 ")
        else:
            f.write(str(dict_kanfang[list2[15]])+" ")
        # 所在楼层
        high0 = re.findall("([0-9]*)", list2[16])
        # 总楼层
        high1 = re.findall("(.*)层", list2[17])
        # 总楼层除以三的结果
        high_class = float(high1[0])/3
        if high0[0]:
            if float(high0[0]) < high_class:
                f.write(str(dict_high["低楼层"])+" ")
            elif float(high0[0]) < high_class*2:
                f.write(str(dict_high["中楼层"])+" ")
            else:
                f.write(str(dict_high["高楼层"])+" ")
        else:
            f.write(str(dict_high[list2[16]])+" ")
        f.write(high1[0]+" ")
        # 电梯
        if list2[18] == "NULL":
            f.write("0 ")
        else:
            f.write(str(dict_dianti[list2[18]])+" ")
        if list2[19] == "NULL":
            f.write("0 ")
        else:
            f.write(str(dict_chewei[list2[19]])+" ")  # 车位
        if list2[20] == "NULL":
            f.write("0 ")
        else:
            f.write(str(dict_yongshui[list2[20]])+" ")  # 用水
        if list2[21] == "NULL":
            f.write("0 ")
        else:
            f.write(str(dict_yongdian[list2[21]])+" ")  # 用电
        if list2[22] == "NULL":
            f.write("0 ")
        else:
            f.write(str(dict_ranqi[list2[22]])+" ")  # 燃气
        if list2[23]=="NULL":
            f.write("0\n")
        else:
            f.write(str(dict_gongnuan[list2[23]])+"\n")  # 供暖