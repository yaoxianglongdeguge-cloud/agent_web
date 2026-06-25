from pathlib import Path
import sys

stay_dir=Path(__file__).parent
current_dir=Path(__file__).parent.parent

sys.path.insert(0, str(current_dir))

from memory_ai import ai_self

def memory_agent(myname:str):
    
    print("已调用记忆概括ai",flush=True)

    my_path=current_dir/myname
    memory_txt=my_path/"memory.txt"
    role_txt=my_path/"role.txt"

    with open(memory_txt,'r',encoding='utf-8') as f:
        memory=f.read()
    with open(role_txt,'r',encoding='utf-8') as f:
        role=f.read()
  
    out_input="我是:"+myname+"这是我的设定："+role+"。"+"这是我的记忆"+memory+"。"+"你帮我概括精简一下。"
    ai_speak1,solve_result1=ai_self.other_run_self(myname,out_input)
    print(ai_speak1, flush=True)

    for line in sys.stdin:
         line = line.strip()
         if not line:
          continue
         
         if line=="quit":
            break
         ai_speak2,solve_result2=ai_self.other_run_self(myname,line)
         print(ai_speak2, flush=True)

    





    