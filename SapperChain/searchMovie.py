import re
import requests
from bs4 import BeautifulSoup
import json

def extract_movie_id(url):
    pattern = r"/subject/(\d+)/"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None


def CrawlerMovie(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'
    }

    response = requests.get(url, headers=headers)
    content = response.text

    soup = BeautifulSoup(content, "html.parser")

    reviews = "id,评论内容" + "\n"

    # 使用find_all方法找到所有的<p>标签
    # p_tags = soup.find_all('p')
    #
    # # 遍历每个<p>标签，判断是否包含目标<span>标签，并提取内容
    # for p_tag in p_tags:
    #     span_tag = p_tag.find('span', class_='pl')
    #     if span_tag and span_tag.text == "类型:":
    #         content = p_tag.get_text(strip=True).replace("类型:", "")
    #         list_content = content.split(",")
    #         # print(list_content[0])
    #         reviews += "电影类型,"+list_content[0] + "\n" + "id,评论内容" + "\n"

    # 获取所有的电影评论
    all_reviews = soup.findAll("span", class_="short")
    i = 0
    while(i < 20):
        review_string = all_reviews[i].string
        # print(review_string)
        reviews += str(i+1)+ "," + review_string + "\n"
        i += 1
    return reviews

def getPromptParams(prompt_template):
    paraNames = []
    if re.search(r"{{\w+}}", prompt_template):
        paraNames = re.findall(r"{{.*}}", prompt_template)
        for i in range(len(paraNames)):
            paraNames[i] = paraNames[i][2:-2]
    return paraNames

def GetMovieReview(promptvalue, preunits, model, debugvalue):
    ready_prompt = promptvalue
    para_name = getPromptParams(promptvalue)
    for index, key in enumerate(para_name):
        ready_prompt = ready_prompt.replace("{{%s}}" % key, preunits[index])
    if debugvalue != "":
        ready_prompt = debugvalue
    print(ready_prompt)
    q = ready_prompt.strip('\n').split("\n")

    # ----------------------------------------------------------------
    # 获取电影名称
    MovieName = q
    # ----------------------------------------------------------------

    result = []
    for i in range(0, len(q)):
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": "00f2b94923c38ae60af53499c0e34b6c615837d1",
            "Content-Type": "application/json"
        }
        data = {
            "q": "豆瓣网电影短评： " + q[i],
            "gl": "cn",
            "hl": "zh-cn"
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            # 请求成功
            response_data = response.json()
            id = extract_movie_id(response_data["organic"][0]["link"])
            url = "https://movie.douban.com/subject/" + id + "/comments?status=P"
            result.append(CrawlerMovie(url))
            # -----------------------------------------------
            # 增加电影名称
            result[i] = "电影名称," + MovieName[i] + "\n" + result[i]
            # -----------------------------------------------
        else:
            # 请求失败
            print(f"请求失败，状态码：{response.status_code}")
            print(response.text)

    return str(result)

# preunits = '#*#*流浪地球'.split("#*#*")
# preunits.reverse()
# preunits.pop()
# preunits.reverse()

# prompt = '{{sds}}\n'
# MovieReview = GetMovieReview(prompt, preunits, '1', '')
# print(len(eval(MovieReview)))
# for movie in eval(MovieReview):
#     print(movie)


# print(GetMovieReview("{{sd}}\n", "", "", ["流浪地球"]))

