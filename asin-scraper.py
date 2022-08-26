from requests_html import HTMLSession
import pandas as pd

url = 'https://www.amazon.co.uk/s?k=nvme+1tb'

s = HTMLSession()
r = s.get(url)
r.html.render(sleep=1)
items = r.html.find('div[data-asin]')

asins = []

for item in items:
    if item.attrs['data-asin'] != '':
        asins.append(item.attrs['data-asin'])

products = []

for asin in asins:
    url = f'https://www.amazon.co.uk/dp/{asin}'
    s = HTMLSession()
    r = s.get(url)
    r.html.render(sleep=1)

    title = r.html.find('#productTitle', first=True).full_text.strip()
    try:
        price = r.html.find('#priceblock_saleprice', first=True).full_text
    except:
        price = r.html.find('#priceblock_ourprice', first=True).full_text

    rating = r.html.find('span.a-icon-alt', first=True).full_text
    reviews = r.html.find('#acrCustomerReviewText', first=True).full_text

    product = {
        'title': title,
        'price': price,
        'rating': rating,
        'reviews': reviews
        }

    products.append(product)
    print('Grabbed ASIN', asin)

df = pd.DataFrame(products)
df.to_csv('ssd.csv', index=False)
