# -*- coding:utf-8 -*-

import requests
import bs4
from bs4 import BeautifulSoup
import io
import csv
import re

index = 0
wf = io.open('idus_item_list.csv', 'wb')
writer = csv.writer(wf)
writer.writerow([index, 'thumbnail_520', 'thumbnail_720', 'thumbnail_list_320', 'title', 'seller', 'cost', 'discount_cost', 'discount_rate', 'description'])

rf = io.open('idus_item_url.csv','rb')
reader = csv.reader(rf)
for URL_BASE in reader:
    req = requests.get(URL_BASE[0])
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    p = re.compile('url\((.*)\)')
    # 이미지 리스트 - 320사이즈
    product_image = soup.select(
        '#content > div.inner-w.layout-split > section.prd-imgs > div > fieldset > ul'
    )[0].children

    image_thumbnail_list_320 = []
    for child in product_image:
        if type(child) is not bs4.element.NavigableString:
            
            image_style = child
            url = p.findall(image_style.get('style'))[0]
            image_thumbnail_list_320.append(url.encode('utf-8'))

    image_thumbnail_520 = image_thumbnail_list_320[0].split('_')[0] + '_520.jpg'
    image_thumbnail_720 = image_thumbnail_list_320[0].split('_')[0] + '_720.jpg'
    # 문자열로 바꾼 이미지 리스트
    image_list = '#'.join(image_thumbnail_list_320)

    # 가격 (원가, 할인가, 할인률)
    # cost_size = 3 -> cross: 원가, strong: 할인가, point: 할인율
    # cost_size = 1 -> strong : 원가 나머지 None
 
    product_cost = soup.select(
        '#content > div.inner-w.layout-split > section.ui-product-detail > div.prd-cost > span.txt-cross'
    )
    if product_cost:
        product_cost = product_cost[0].text.encode('utf-8')
    else: product_cost = None

    product_discount_cost = soup.select(
        '#content > div.inner-w.layout-split > section.ui-product-detail > div.prd-cost > span.txt-strong'
    )[0].text.encode('utf-8')

    product_discount_rate = soup.select(
        '#content > div.inner-w.layout-split > section.ui-product-detail > div.prd-cost > span.txt-point'
    )
    if product_discount_rate:
        product_discount_rate = product_discount_rate[0].text.encode('utf-8')
    else: product_discount_rate = None 

    if product_discount_rate == None and product_cost == None:
        product_cost = product_discount_cost
        product_discount_cost = None

    # 상품명
    product_title = soup.select(
        '#content > div.inner-w.layout-split > section.ui-product-detail > h1'
    )[0].text.encode('utf-8')
    # 셀러
    product_seller = soup.select(
        '#content > div.inner-w.layout-split > section.ui-product-detail > div.circ-card > a.circ-label.fl > span'
    )[0].text.encode('utf-8')
    # 설명
    product_description = soup.select(
        '#prd-info > p'
    )[0].text.encode('utf-8')

    index += 1
    writer.writerow([
        index,
        image_thumbnail_520,
        image_thumbnail_720,
        image_list,
        product_title,
        product_seller,
        product_cost,
        product_discount_cost,
        product_discount_rate,
        product_description
    ])

    print(str(product_title) + ' 완료 !!')

    # print(image_thumbnail_520)
    # print(image_thumbnail_720)
    # print(image_list)

    # print(product_title)
    # print(product_seller)
    # print(product_cost)
    # print(product_discount_cost)
    # print(product_discount_rate)
    # print(product_description)

rf.close()
wf.close()

