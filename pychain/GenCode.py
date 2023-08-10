from sapperchain import sapperchain
import os
import json
from flask import jsonify

file_path = os.path.join(os.path.dirname(__file__), 'storage.json')


def read_json():
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def write_json(data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def update_request(initrecord, query):
    initrecord["id"] = query['id']
    initrecord["runflag"] = True
    data = read_json()
    has_id = False
    for record in data:
        if record['id'] == query['id']:
            has_id = True
            return record
    if not has_id:
        new_record = initrecord
        data.append(new_record)
        write_json(data)
        return new_record


def get_value(vary, request, query):
    if vary == query["input"]:
        query["runflag"] = True
        query["input"] = ""
        query[vary] = request["query"]
        return False, query, request["query"]
    else:
        return True, query, query[vary]


def resetquery(query,initrecord):
    initrecord["id"] = query['id']
    initrecord["runflag"] = True
    query = initrecord
    data = read_json()
    for i in range(len(data)):
        record = data[i]
        if record['id'] == query['id']:
            data[i] = query
    write_json(data)


def savequery(query):
    data = read_json()
    for i in range(len(data)):
        record = data[i]
        if record['id'] == query['id']:
            data[i] = query
    write_json(data)



f1 = open("pychain/PromptTemplate.json", "r", encoding='UTF-8')
prompt_template = json.loads(f1.read())


def sapper(sapper_request):
    chain = sapperchain(sapper_request['OpenaiKey'])
    chain.promptbase(prompt_template)

    initrecord = {"id":"","input":"preInfo","output":[],"runflag":"","Poetry_Lines":"","Artistic_Conception1":"","Artistic_Conception2":"","Artistic_Conception3":"","Refined_Artistic_Conception":"","Concise_Phrases":"","Suitable_Phrases":"","Painting_Style":"","Style_Characteristics1":"","Style_Characteristics2":"","Style_Characteristics3":"","preInfo":""}
    sapper_query = update_request(initrecord, sapper_request)
    Poetry_Lines=sapper_query["Poetry_Lines"]
    Artistic_Conception1=sapper_query["Artistic_Conception1"]
    Artistic_Conception2=sapper_query["Artistic_Conception2"]
    Artistic_Conception3=sapper_query["Artistic_Conception3"]
    Refined_Artistic_Conception=sapper_query["Refined_Artistic_Conception"]
    Concise_Phrases=sapper_query["Concise_Phrases"]
    Suitable_Phrases=sapper_query["Suitable_Phrases"]
    Painting_Style=sapper_query["Painting_Style"]
    Style_Characteristics1=sapper_query["Style_Characteristics1"]
    Style_Characteristics2=sapper_query["Style_Characteristics2"]
    Style_Characteristics3=sapper_query["Style_Characteristics3"]
    preInfo=sapper_query["preInfo"]
    sapper_query["output"] = []
    if sapper_query["runflag"]:
        preInfo = """ palette, brush strokes, texture, and composition."]]}
    
    Hi there! Welcome to our small AI service that helps to create artistic conceptions based on poetry. To get started, please input a few lines of poetry that you'd like us to work with. We'll use these lines as a starting point to generate an artistic conception that conveys a mood or emotion. Let's get started!"""
        sapper_query["preInfo"]=preInfo
    if sapper_query["runflag"]:
        sapper_query["output"].append(preInfo)
        stop, sapper_query, Unit = get_value("preInfo", sapper_request, sapper_query)
    stop, sapper_query, Poetry_Lines = get_value("Poetry_Lines", sapper_request, sapper_query)
    if stop and sapper_query["runflag"]:
        sapper_query["runflag"] = False
        sapper_query["input"] = "Poetry_Lines"
        savequery(sapper_query)
        return {'Answer': sapper_query["output"]}
    if sapper_query["runflag"]:
        Artistic_Conception1 = chain.worker("OJ{aW;e,aWljr$aM`^Z?",[Poetry_Lines],{"temperature":0.7,"max_tokens":225,"top_p":1,"frequency_penalty":0,"presence_penalty":0,"engine":" gpt-3.5-turbo"})
        sapper_query["Artistic_Conception1"]=Artistic_Conception1
    if sapper_query["runflag"]:
        Artistic_Conception2 = chain.worker("T5/h(PiL]WpvE=5ON/5k",[Poetry_Lines],{"temperature":0.7,"max_tokens":225,"top_p":1,"frequency_penalty":0,"presence_penalty":0,"engine":" gpt-3.5-turbo"})
        sapper_query["Artistic_Conception2"]=Artistic_Conception2
    if sapper_query["runflag"]:
        Artistic_Conception3 = chain.worker("-rYL3;_Hu.|P.,WP3$3B",[Poetry_Lines],{"temperature":0.7,"max_tokens":225,"top_p":1,"frequency_penalty":0,"presence_penalty":0,"engine":" gpt-3.5-turbo"})
        sapper_query["Artistic_Conception3"]=Artistic_Conception3
    if sapper_query["runflag"]:
        Refined_Artistic_Conception = chain.worker("Ik#qLbnB][y(WQnp7BJ[",[Artistic_Conception1,Artistic_Conception2,Artistic_Conception3],{"temperature":0.7,"max_tokens":225,"top_p":1,"frequency_penalty":0,"presence_penalty":0,"engine":" gpt-3.5-turbo"})
        sapper_query["Refined_Artistic_Conception"]=Refined_Artistic_Conception
    if sapper_query["runflag"]:
        Concise_Phrases = chain.worker("LL}ml^,:dalgV;z6).e5",[Refined_Artistic_Conception],{"temperature":0.7,"max_tokens":225,"top_p":1,"frequency_penalty":0,"presence_penalty":0,"engine":" gpt-3.5-turbo"})
        sapper_query["Concise_Phrases"]=Concise_Phrases
    if sapper_query["runflag"]:
        Suitable_Phrases = chain.worker("(~^sRk4A2g2f`jFczSnw",[Concise_Phrases],{"temperature":0.7,"max_tokens":225,"top_p":1,"frequency_penalty":0,"presence_penalty":0,"engine":" gpt-3.5-turbo"})
        sapper_query["Suitable_Phrases"]=Suitable_Phrases
    if sapper_query["runflag"]:
        Painting_Style = chain.worker("(iQ[LaZRx_LFF8-djt~q",[Poetry_Lines],{"temperature":0.7,"max_tokens":225,"top_p":1,"frequency_penalty":0,"presence_penalty":0,"engine":" gpt-3.5-turbo"})
        sapper_query["Painting_Style"]=Painting_Style
    if sapper_query["runflag"]:
        Style_Characteristics1 = chain.worker("o%)m_zuCA@=e=jb;0h-Z",[Painting_Style],{"temperature":0.7,"max_tokens":225,"top_p":1,"frequency_penalty":0,"presence_penalty":0,"engine":" gpt-3.5-turbo"})
        sapper_query["Style_Characteristics1"]=Style_Characteristics1
    if sapper_query["runflag"]:
        Style_Characteristics2 = chain.worker("VBw549LRw$=WoQ{vy+3b",[Poetry_Lines,Painting_Style],{"temperature":0.7,"max_tokens":225,"top_p":1,"frequency_penalty":0,"presence_penalty":0,"engine":" gpt-3.5-turbo"})
        sapper_query["Style_Characteristics2"]=Style_Characteristics2
    if sapper_query["runflag"]:
        Style_Characteristics3 = chain.worker("8o+8E3SnWDO~#z0[T823",[Suitable_Phrases,Painting_Style,Style_Characteristics1,Style_Characteristics2],{"temperature":0.7,"max_tokens":225,"top_p":1,"frequency_penalty":0,"presence_penalty":0,"engine":" DALL-E"})
        sapper_query["Style_Characteristics3"]=Style_Characteristics3
    if sapper_query["runflag"]:
        sapper_query["output"].append(Style_Characteristics3)
    


    resetquery(sapper_query, initrecord)
    return {'Answer': sapper_query["output"]}
