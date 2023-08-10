import matplotlib.pyplot as plt
import csv
import re
import random
import string
import uuid  # 导入uuid模块

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# random_8_chars = generate_random_string(8)
# print(random_8_chars)


# 示例数据
def DrawMovie21(data_str):
    categories = []
    values = []
    # 将输入字符串转换为可计算的数据结构
    data = list(csv.reader(data_str.strip().splitlines()))

    # 从第二列开始获取评论分数并转换为整数
    scores = {}
    for row in data[1:]:
        movie_type = row[0]
        scores[movie_type] = [int(score) for score in row[1:]]

    # 计算每个电影类型的平均分
    for movie_type, score_list in scores.items():
        average_score = sum(score_list) / len(score_list)
        categories.append(movie_type)
        values.append(average_score)
        print(f"Movie Type: {movie_type}, Average Score: {average_score}")

    plt.clf()
    # 创建柱状图
    plt.bar(categories, values)

    # 添加标签和标题
    plt.xlabel('Movie Genre')
    plt.ylabel('Average Score')
    plt.title('Score for each Movie Genre')

    # 在柱状图上标明数值
    for index, value in enumerate(values):
        plt.text(index, value, str(value), ha='center', va='bottom')

    # 显示图形
    path = "static/movieImages/" + str(uuid.uuid4()) + '.png'
    plt.savefig(path)
    return path
    # plt.show()

def getPromptParams(prompt_template):
    paraNames = []
    if re.search(r"{{\w+}}", prompt_template):
        paraNames = re.findall(r"{{.*}}", prompt_template)
        for i in range(len(paraNames)):
            paraNames[i] = paraNames[i][2:-2]
    return paraNames

def drawData(promptvalue, preunits, model, debugvalue):
    ready_prompt = promptvalue
    para_name = getPromptParams(promptvalue)
    for index, key in enumerate(para_name):
        ready_prompt = ready_prompt.replace("{{%s}}" % key, preunits[index])
    if debugvalue != "":
        ready_prompt = debugvalue
    print(ready_prompt)
    path = DrawMovie21(ready_prompt)
    return path

# csv_data = """Movie Type, Review 1, Review 2, Review 3, Review 4, Review 5, Review 6, Review 7, Review 8, Review 9, Review 10
# War, 0, 10, 0, 5, 5, 0, 0, 10, 0, 10
# Comedy, 0, 10, 10, 10, 10, 0, 0, 0, 10, 10
# Story, 0, 10, 10, 0, 0, 10, 10, 10, 0, 0
# Child, 10, 0, 0, 10, 10, 0, 0, 10, 10, 10
# """
# 
# drawData('{{ds}}', [csv_data], '1', '')
