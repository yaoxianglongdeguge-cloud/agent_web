from pathlib import Path#不能直接用，只能用来引导路径
import shutil
import importlib
import importlib.util
import sys

agents=sys.argv[1]
myname=sys.argv[2]
action=sys.argv[3]
tool=sys.argv[4]

current_dir=Path(__file__).parent.parent/"agents"/agents
sys.path.insert(0, str(current_dir))


from port import desmake_port

if __name__=="__main__":
  
   desmake_port.tools_make(myname,action,tool)


   
  
        
  
 


