import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_amazon_data():
    # 设置请求头部信息，模拟浏览器访问
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # 定义要爬取的页面URL
    url = 'https://www.amazon.com/s?k=%E6%99%BA%E8%83%BD%E5%AE%B6%E5%B1%85&crid=2TJSSYPRUR2NG&sprefix=znjj%2Caps%2C384&ref=nb_sb_noss_2'

    # 发送请求
    response = requests.get(url, headers=headers)

    # 使用BeautifulSoup解析页面
    soup = BeautifulSoup(response.text, 'html.parser')

    # 初始化数据存储列表
    products = []

    # 找到所有商品列表项
    for i in soup.find_all("div", attrs={"data-component-type": "s-search-result"}):
        # 提取商品名称
        name = i.find("span", class_="a-size-medium a-color-base a-text-normal")
        name = name.text if name else "No Name"

        # 提取价格
        price = i.find("span", class_="a-price-whole")
        price = f'{price.text}{price.find("span", class_="a-price-fraction").text}' if price else "No Price"

        # 提取星级
        rating = i.find("span", class_="a-icon-alt")
        rating = rating.text if rating else "No Rating"

        # 提取评价数量
        rating_count = i.find("span", class_="a-size-base")
        rating_count = rating_count.text if rating_count else "No Rating Count"

        # 将提取的数据添加到列表
        products.append([name, rating, price, rating_count])

    return products


# 获取数据
data = get_amazon_data()

# 创建DataFrame
df = pd.DataFrame(data, columns=["Name", "Rating", "Price", "Rating Count"])

# 写入Excel文件
df.to_excel('D:/Amazon.xlsx', index=False)

print("Data scraped and saved to D:/Amazon.xlsx")
