import os,sys
# Path ./DSA-Bootcamp-Java/lectures/
par=sys.argv[1]
icon=False if sys.argv[2].lower()=="false" else True
num=False if sys.argv[3].lower()=="false" else True
folder_icon='📁' 
file_icon='📄'
if (len(sys.argv)>=5):
   folder_icon=sys.argv[4] if sys.argv[4] else '📁' 
if (len(sys.argv)>=6):
    file_icon=sys.argv[5] if sys.argv[5] else '📄'
def gen_index(path):
    dirs=os.listdir(path)
    try:
                value="## Tables of content\n"
                c_dirs=os.listdir(os.path.join(path))
                print(c_dirs)
                for c_dir in c_dirs:
                    c_path=os.path.join(path,c_dir)
                    if not os.path.isfile(c_path):
                          ch_dir=c_dir.strip().replace(" ","%20")
                          value+=f"{'1.' if num else '- '}{folder_icon if icon else ''} [{c_dir}](./{ch_dir})\n"
                          gen_index(c_path)
                          
                    else:
                        ch_dir=c_dir.strip().replace(" ","%20")
                        if c_dir!="readme.md":
                           value+=f"{'1.' if num else '- '}{file_icon if icon else ''} [{c_dir}](./{ch_dir})\n"
                readme=os.path.join(path,"readme.md")
                print(readme)
                with open(readme,"w",encoding='utf-8') as file:
                        file.write(value)
                        print("Written:\n",value)
    except Exception as e:
            print(e,"Missed something or tried to open list readme.md")
gen_index(par)
