from ai_generate import ai_generate
import json
import sys

action=sys.argv[1]
name=sys.argv[2]
role=sys.argv[3]

if __name__ == "__main__":
 
    if action=="create":

       reply=ai_generate.new_ai(name,role)
       if reply==0:
          print("禁止与基本文件重名！")
          sys.exit(1)
       
       try:
        with open("agent_login.json", "r", encoding="utf-8") as f:
            agents = json.load(f)
       except FileNotFoundError:
          agents = []
        
       agents.append(name)

       with open("agent_login.json",'w',encoding='utf-8') as f:
         json.dump(agents,f,ensure_ascii=False, indent=2)
       

    elif action=="delete":
         
         reply=ai_generate.delete_ai(name)

         if reply==3:
          print("禁止删除基本文件！")
          sys.exit(2)
          
         try:
          with open("agent_login.json", "r", encoding="utf-8") as f:
            agents = json.load(f)
         except FileNotFoundError:
          agents = []
         if name in agents:
          agents.remove(name)
         with open("agent_login.json",'w',encoding='utf-8') as f:
          json.dump(agents,f,ensure_ascii=False, indent=2)

      

      
      

