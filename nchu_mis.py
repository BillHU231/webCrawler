import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup

# 網址
url = "https://mis.nchu.edu.tw/tag/%e7%a2%a9%e5%a3%ab%e9%81%9e%e8%a3%9c"
# 設定寄件者、收件者的電子郵件地址
sender_email = "billhu0915@gmail.com"
receiver_email = "asbill920166@gmail.com"
password = "phcu lkdp eohb nrkj"

# 發送 GET 請求
response = requests.get(url)

# 設定郵件的內容
subject = "中興大學最新備取"
body = " "

# 建立 MIME 物件
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# 確認網頁請求成功
if response.status_code == 200:
    # 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找 id 為 "blog-entries" 的 div 標籤
    blog_entries_div = soup.find('div', id='blog-entries')

    # 如果找到了該 div 標籤，則找出其中所有的 article 標籤並列印其 id
    if blog_entries_div:
        articles = blog_entries_div.find_all('article')
        for article in articles:
            article_id = article.get('id')
            if article_id:  # 如果有 id 屬性
                article_id_num = int(article_id[5:-1])

                if article_id_num > 1078:

                  h2_tag= article.find('h2')
                  url = h2_tag.find('a').get('href')
                  body+= "最新備取 url : " + url
                else:
                  body+= "未有最新備取進度"
                break

    else:
        print("未找到 id 為 'blog-entries' 的 div 標籤。")
        body+= "未找到 id 為 'blog-entries' 的 div 標籤。"
else:
    print(f"無法獲取網頁，狀態碼: {response.status_code}")
    body+= f"無法獲取網頁，狀態碼: {response.status_code}"


# 附加郵件內容
message.attach(MIMEText(body, "plain"))
# 連接到 Gmail 的 SMTP 伺服器並寄送郵件
try:
  with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
     server.login(sender_email, password)
     server.sendmail(sender_email, receiver_email, message.as_string())
     print("郵件已發送成功！")
except Exception as e:
      print(f"郵件發送失敗: {e}")