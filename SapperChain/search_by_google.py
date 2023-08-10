# !/user/bin/env python3
# -*- coding: utf-8 -*-
import http.client
import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import openai
from TextSplitter import RecursiveCharacterTextSplitter

load_dotenv()
browserless_api_key = os.getenv("BROWERLESS_API_KEY")
serper_api_key = os.getenv("SERP_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
def add_message(role_name: str, role_message: str, messages: list = None):
    if messages is None:
        messages = []
    messages.append({"role": role_name, "content": role_message})
    return messages

def search(query):
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
        "q": query
    })
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return data.decode("utf-8")

def chatgpt(messages):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return (response['choices'][0]['message']['content'])

def scrape_website(objective: str, url: str):
     # scrape the website, and also will summarize the content based on the objective (e.g. summarize the content based on the objective)
     # objective is the objective & task that user give to the agent, url is the url of the website that user want to scrape
     print("Scraping website..." + url)
     # Define the headers for the request
     headers = {
         'Cache-Control': 'no-cache',
         'Content-Type': 'application/json',
     }

     # Define the data to be sent in the request
     data = {
        "url": url
     }

     # Convert Python Object to JSON
     data_json = json.dumps(data)

     # Send the POST request
     post_url = f"https://chrome.browserless.io/content?token={browserless_api_key}"
     response = requests.post(post_url, headers=headers, data=data_json)

     # Check the response status code
     if response.status_code == 200:
         soup = BeautifulSoup(response.content, 'html.parser')
         text = soup.get_text()
         # print("Content:", text)

         if len(text) > 10000:
             output = summary(objective, text)
             return output
         return text
     else:
         print(f"HTTP requset failed with status code: {response.status_code}")

def summary(objective, content):
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=10000, chunk_overlap=500)
    docs = text_splitter.create_documents([content])
    summary_prompt_template = """
    Write a summary of the following text for {objective}:
    "{text}"
    SUMMARY:
    """
    # 把每一段的summary都加入到prompt中
    all_summary = "\n".join(
        chatgpt(add_message("user", summary_prompt_template.format(objective=objective, text=doc.page_content)))
        for doc in docs
    )

    all_summary_prompt_filled = summary_prompt_template.format(objective=objective, text=all_summary)
    output = chatgpt(add_message("user", all_summary_prompt_filled))

    return output

def search_by_google(user_query: str):
    system_message = """You are a world class researcher, who can do detailed research on any topic and produce facts based results; 
                you do not make things up, you will try as hard as possible to gather facts & data to back up the research

                Please make sure you complete the objective above with the following rules:
                1/ You should do enough research to gather as much information as possible about the objective
                2/ If there are url of relevant links & articles, you will scrape it to gather more information
                3/ After scraping & search, you should think "is there any new things i should search & scraping based on the data I collected to increase research quality?" If answer is yes, continue; But don't do this more than 3 iteratins
                4/ You should not make things up, you should only write facts & data that you have gathered
                5/ In the final output, You should include all reference data & links to back up your research; You should include all reference data & links to back up your research
                6/ In the final output, You should include all reference data & links to back up your research; You should include all reference data & links to back up your research"""
    messages = add_message("system", system_message)

    # update the message
    messages = add_message("user", user_query, messages)

    search_result = search(user_query)
    search_result = json.loads(search_result)
    links = [item["link"] for item in search_result["organic"][:3]]  # 只获取前三个链接

    # 初始化一个空列表用于存储每个链接的总结信息
    search_and_summary_results = []

    for link in links:
        content = scrape_website(user_query, link)
        summary_result = summary(user_query, content)
        search_and_summary_result = link + "\n" + summary_result

        # 将每个链接的总结信息添加到列表中
        search_and_summary_results.append(search_and_summary_result)

    # update the message
    messages = add_message("system", "\n".join(search_and_summary_results), messages)
    result = chatgpt(messages)
    return result

if __name__ == '__main__':
    user_query = "电影流浪地球的电影短评，豆瓣网"
    print(search_by_google(user_query))
