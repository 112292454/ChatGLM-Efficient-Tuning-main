import json
"S Expression"
#转sparql
# history=[['You are a knowledge base question answearing expert. Convert the following question into the corresponding SPARQL query. Instead of using Mid in the generated sparql statement, use the entity and relationship names in the question.',"Ok, give me the question, I'll give you the Sparql statement, and I'll avoid using Mid in sparql statements"],
#          ["Generate a SPARQL query that retrieves the information corresponding to the given question:[what does jamaican people speak]","PREFIX ns: <http://rdf.freebase.com/ns/>\nSELECT DISTINCT ?x\nWHERE {\nFILTER (?x != ns:Jamaica)\nFILTER (!isLiteral(?x) OR lang(?x) = '' OR langMatches(lang(?x), 'en'))\nns:Jamaica ns:location.country.languages_spoken ?x .\n}\n"]]
# 


history=[]

base_dir="F:\正事\科研训练\ChatGLM-Efficient-Tuning-main/"

# json_file_path = base_dir+'data/WebQSP/WebQSP_test.json'  # 替换为实际的文件路径
json_file_path = base_dir+'data/generated_predictions.jsonl'  # 替换为实际的文件路径
data_batch = []



def remove_dup():
    instruction = "Generate a SPARQL query that retrieves the information corresponding to the given question:"
    for item in json_data:
        input="%s"%item["content"]
        #history=item["history"]
        #history.clear()
        output="%s"%item["summary"]

        input=input.replace("Generate a SPARQL query that retrieves the information corresponding to the given question:[","")
        input=input.removesuffix("]")

        output=output.replace("PREFIX ns: <http://rdf.freebase.com/ns/>\n","")
        output.replace(" ?","   ?")
        print(input+"\n==>   "+output)

        now={}
        now['instruction']=instruction
        now['input'] = input
        now["output"] = output
        #now["history"]=history
        data_batch.append(now)
    with open(base_dir+"data/WebQSP/result/WebQSP_test.json", "w", encoding="utf-8") as file:
        json.dump(data_batch, file)

def check_equal_rate():
    i=0
    n=0
    for item in json_data:
        label="%s"%item['label']
        predict=item['predict']
        n+=1
        if label.__eq__(predict):
            i+=1
    print('rate:',i*1.0/n)

def load_from_CCKS():
    ins = "生成一个 SPARQL 查询，检索与以下给定问题对应的信息："

    with open("C://Users\gzy\Documents\WeChat Files\wxid_uuci6i8jdt3o22\FileStorage\File/2023-07/test2.txt", 'r', encoding="utf-8") as file:
        lines=file.readlines()
        data=[]
        for i,item in enumerate(lines):
            item=item.replace("\n","")
            now={}
            now['instruction'] = ins
            now['input'] = item
            now["output"] = ""
            data.append(now)


        with open(base_dir + "data/CCKS/process/test2.json", "w", encoding="utf-8") as file:
            json.dump(data, file,ensure_ascii=False,indent=4)






if __name__ == "__main__":
    load_from_CCKS()
    # load_from_CCKS()
    with open("F:\正事\科研训练\ChatGLM-Efficient-Tuning-main\data\CCKS/process/train.txt", 'r', encoding="utf-8") as file:
        lines = file.readlines()
        data = []
        res=[]
        for i, item in enumerate(lines):
            item = item.replace("\n", "")

            if i%2==0:
                data.append(item)
            if i%2==1:
                res.append(item)

        with open(base_dir + "data/CCKS/process/question.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        with open(base_dir + "data/CCKS/process/answer.json", "w", encoding="utf-8") as file:
            json.dump(res, file, ensure_ascii=False, indent=4)


    with open(json_file_path, 'r', encoding="utf-8") as file:
        json_data = json.load(file)

    check_equal_rate()

# for item in json_data['Questions']:
#     # 在这里处理每个 JSON 对象
#     # print(item)
#     content="Generate a SPARQL query that retrieves the information corresponding to the given question:"
#     input="%s"%item["ProcessedQuestion"]
#     for j in item["Parses"]:
#         now = {}
#         now['instruction']=content
#         now['input']=input
#         sparql=j["Sparql"]
#         #替换里面的mid
#         if j["TopicEntityName"]!=None:
#             sparql=sparql.replace(j["TopicEntityMid"],j["TopicEntityName"])
#         #有Constraints时也替换
#         for i in j["Constraints"]:
#             if i["EntityName"] is None:#有时候会为null无需操作
#                 continue
#             sparql = sparql.replace(i["Argument"],i["EntityName"])
#
#         if sparql.startswith("#MANUAL SPARQL\n"):
#             sparql=sparql[15:]
#
#         now["output"]=sparql
#
#         now["history"]=history
#         data_batch.append(now)
#         break



# 结果写入
# with open("data/WebQSP/sparql_tuning/WebQSP.test.sparql.json", "w", encoding="utf-8") as file:
#     json.dump(data_batch, file)

#===============================================================================================================
    # for item in data_batch:
    #     line = json.dumps(item, ensure_ascii=False)
    #     file.write(line + "\n")
        # break


# history=[]


# json_file_path = 'data/WebQSP/origin/WebQSP.test.json'  # 替换为实际的文件路径
# data_batch = []
# with open(json_file_path, 'r', encoding="utf-8") as file:
#     json_data = json.load(file)

# for item in json_data['Questions']:
#     # 在这里处理每个 JSON 对象
#     # print(item)
#     content="Generate a SPARQL query that retrieves the information corresponding to the given question:[%s]"%item["ProcessedQuestion"]
#     for j in item["Parses"]:
#         now = {}
#         now['content']=content
#         sparql=j["Sparql"]
#         #替换里面的mid
#         if j["TopicEntityName"]!=None:
#             sparql=sparql.replace(j["TopicEntityMid"],j["TopicEntityName"])
#         #有Constraints时也替换
#         for i in j["Constraints"]:
#             if i["EntityName"] is None:#有时候会为null无需操作
#                 continue
#             sparql = sparql.replace(i["Argument"],i["EntityName"])

#         now["summary"]=sparql

#         now["history"]=history
#         data_batch.append(now)



# #结果写入
# with open("data/WebQSP/sparql_tuning/WebQSP.test.sparql.json", "w", encoding="utf-8") as file:
#     for item in data_batch:
#         line = json.dumps(item, ensure_ascii=False)
#         file.write(line + "\n")
#         # break

#转中间结果
# history2=[['You are a knowledge base question answearing expert. Convert the following question into the corresponding S-expression(SExpr) query. Instead of using Mid in the generated S-expression(SExpr) statement, use the entity and relationship names in the question.',"Ok, give me the question, I'll give you the S-expression(SExpr) statement, and I'll avoid using Mid in S-expression(SExpr) statements"],
#          ["Generate a S-expression(SExpr) query that retrieves the information corresponding to the given question:[what does jamaican people speak]","(JOIN (R location.country.languages_spoken) Jamaica)"]]
# #

# json_file_path = 'sexpr/WebQSP.test.expr.json'  # 替换为实际的文件路径
# data_batch = []
# with open(json_file_path, 'r', encoding="utf-8") as file:
#     json_data = json.load(file)

# for item in json_data:
#     # 在这里处理每个 JSON 对象
#     # print(item)
#     content="Generate a S-expression(SExpr) query that retrieves the information corresponding to the given question:[%s]"%item["ProcessedQuestion"]
#     for j in item["Parses"]:
#         now = {}
#         now['content']=content
#         sparql=j["SExpr"]
#         #替换里面的mid
#         if j["TopicEntityName"]!=None:
#             sparql=sparql.replace(j["TopicEntityMid"],j["TopicEntityName"])
#         #有Constraints时也替换
#         # for i in j["Constraints"]:
#         #     if i["EntityName"] is None:#有时候会为null无需操作
#         #         continue
#         #     sparql = sparql.replace(i["Argument"],i["EntityName"])

#         now["summary"]=sparql

#         # now["history"]=history2
#         data_batch.append(now)



# #结果写入
# with open("data/WebQSP.test.jsonl", "a", encoding="utf-8") as file:
#     for item in data_batch:
#         line = json.dumps(item, ensure_ascii=False)
#         file.write(line + "\n")
#         # break
