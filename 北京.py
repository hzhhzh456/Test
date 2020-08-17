import re
import os
import openpyxl
import requests
from parsel import Selector


def huode_list(num):
    #爬取当前页的房源列表
    url = 'https://bj.zu.ke.com/zufang/pg' + str(num)            # 目标url

    # 请求
    r = requests.get(url)

    # 交给parsel库来解析html
    sel = Selector(r.text)

    # 获取当前页面下的所有链接，区，方位
    a_list = sel.xpath('//a[@class="content__list--item--aside"]/@href').extract()
    dis_list = sel.xpath('//p[@class="content__list--item--des"]/a[1]/text()').extract()
    pos_list = sel.xpath('//p[@class="content__list--item--des"]/a[2]/text()').extract()

    # 排除公寓，只要租房
    zufang_list = []
    for a in a_list:
        if 'zufang' in a:
            zufang_list.append(a)

    # 合并链接，区和方位(区和方位待会传递到crawl_detail函数中)
    final_list = list(zip(zufang_list, dis_list, pos_list))
    print(final_list)
    return final_list


def paqu_detail(final_list):
    #进入每个链接的详情页，爬取目标信息
    base_url = 'https://bj.zu.ke.com/'

    data = []
    for info in final_list:
        url = base_url + info[0]               # 目标详情页url

        # 请求详情页
        r = requests.get(url)

        # 交给parsel库来解析html
        sel = Selector(r.text)

        # 获取当前页面下的信息
        # 房屋编号
        try:
            code = sel.xpath('//i[@class="house_code"]/text()').extract_first()
        except:
            code = 'NULL'

        # 城市
        city = '北京'

        # 区
        try:
            dis = info[1]
        except:
            dis = 'NULL'

        # 方位
        try:
            pos = info[2]
        except:
            pos = 'NULL'

        # 房屋名字
        try:
            name = sel.xpath('//p[@class="content__title"]/text()').extract_first().split('·')[-1].split(' ')[0]
        except:
            name = 'NULL'

        # 入住
        try:
            area = sel.xpath('//div[@class="content__article__info"]/ul[1]/li[2]/text()').extract_first().split('：')[-1]
        except:
            area = 'NULL'

        # 租赁方式
        try:
            rent_way = sel.xpath('//p[@class="content__title"]/text()').extract_first().split('·')[0]
        except:
            rent_way = 'NULL'

        # 朝向
        try:
            face = sel.xpath('//p[@class="content__title"]/text()').extract_first().split('·')[-1].split(' ')[-1]
        except:
            face = 'NULL'

        # 月租
        try:
            month_fee = sel.xpath('//div[@class="content__aside--title"]/span/text()').extract_first()
        except:
            month_fee = 'NULL'

        # 计费方式
        try:
            temp = re.search(r'\(.*\)', sel.xpath('string(//div[@id="aside"]/div[@class="content__aside--title"])').extract_first())
            if temp:
                fee_way = temp.group().replace('(', '').replace(')', '')
            else:
                fee_way = 'NULL'
        except:
            fee_way = 'NULL'

        # 几室
        try:
            bedroom_num = sel.xpath('//ul[@class="content__aside__list"]/li[2]/text()').extract_first()[:2]
        except:
            bedroom_num = 'NULL'

        # 几厅
        try:
            living_num = sel.xpath('//ul[@class="content__aside__list"]/li[2]/text()').extract_first()[2:4]
        except:
            living_num = "NULL"

        # 几卫
        try:
            bathroon_num = sel.xpath('//ul[@class="content__aside__list"]/li[2]/text()').extract_first()[4:6]
        except:
            bathroon_num = 'NULL'

        # 入住
        try:
            move_time = sel.xpath('//div[@class="content__article__info"]/ul[1]/li[6]/text()').extract_first().split('：')[-1]
        except:
            move_time = 'NULL'

        # 租期
        try:
            rent_time = sel.xpath('//div[@class="content__article__info"]/ul[2]/li[2]/text()').extract_first().split('：')[-1]
        except:
            rent_time = 'NULL'

        # 看房
        try:
            watch_time = sel.xpath('//div[@class="content__article__info"]/ul[2]/li[5]/text()').extract_first().split('：')[-1]
        except:
            watch_time = 'NULL'

        # 所在楼层
        try:
            floor1 = sel.xpath('//div[@class="content__article__info"]/ul[1]/li[8]/text()').extract_first().split('：')[-1].split('/')[0]
        except:
            floor1 = 'NULL'

        # 总楼层
        try:
            floor2 = sel.xpath('//div[@class="content__article__info"]/ul[1]/li[8]/text()').extract_first().split('：')[-1].split('/')[1]
        except:
            floor2 = 'NULL'

        # 电梯
        try:
            elevator = sel.xpath('//div[@class="content__article__info"]/ul[1]/li[9]/text()').extract_first().split('：')[-1]
        except Exception as e:
            elevator = 'NULL'

        # 车位
        try:
            parking = sel.xpath('//div[@class="content__article__info"]/ul[1]/li[11]/text()').extract_first().split('：')[-1]
        except:
            parking = 'NULL'

        # 用水
        try:
            water = sel.xpath('//div[@class="content__article__info"]/ul[1]/li[12]/text()').extract_first().split('：')[-1]
        except:
            water = 'NULL'

        # 用电
        try:
            electricity = sel.xpath('//div[@class="content__article__info"]/ul[1]/li[14]/text()').extract_first().split('：')[-1]
        except:
            electricity = 'NULL'

        # 燃气
        try:
            gas = sel.xpath('//div[@class="content__article__info"]/ul[1]/li[15]/text()').extract_first().split('：')[-1]
        except:
            gas = 'NULL'

        # 供暖
        try:
            heat = sel.xpath('//div[@class="content__article__info"]/ul[1]/li[17]/text()').extract_first().split('：')[-1]
        except:
            heat = 'NULL'
        data.append([code, city, dis, pos, name, area, rent_way, face, month_fee, fee_way, bedroom_num, living_num,
                     bathroon_num, move_time, rent_time, watch_time, floor1, floor2, elevator, parking, water,
                     electricity, gas, heat])

    return data


def baocun(data, path):
    #保存数据到excel
    if os.path.exists(path):
        wb = openpyxl.load_workbook(path)
        ws = wb.active
        for d in data:
            ws.append(d)
        wb.save(path)

    else:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['房屋编号', '城市', '区', '方位', '房屋名', '大小', '租赁方式', '朝向', '月租', '计费方式', '几室',
                   '几厅', '几卫', '入住', '租期', '看房', '所在楼层', '总楼层', '电梯', '车位', '用水', '用电', '燃气', '供暖'])
        for d in data:
            ws.append(d)
        wb.save(path)


if __name__ == '__main__':
    for i in range(1, 51):
        print(f'正在爬取第{i}页信息')
        zufang_info = huode_list(i)
        d = paqu_detail(zufang_info)
        print(f'正在保存第{i}页信息')
        baocun(d, './data.xlsx')

    print('保存完毕')