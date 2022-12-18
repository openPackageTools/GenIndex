"""
This module generates indices for github pages. Github repo which false in category of code base more than a static site and
 we try to deploy such files to github pages then for nested folder either we have to create a index.html or a readme to access these code
 bases. This Module help this this particular case.

Customizations:
  1. Page type - page type can be set to html or github markdown 
  2. List type - 
  3. Icon -
  
 
"""
import traceback
import shutil
import os
import sys
# Path ./DSA-Bootcamp-Java/lectures/


class GenIndex:
    def __init__(self, override=False,num=False, icon=False, folder_icon='📁', file_icon='📄', type="MD",debug=False):
        self.num = num
        self.icon = icon
        self.folder_icon = folder_icon
        self.file_icon = file_icon
        self.type = type
        self.debug=debug
        self.gen_ingore=[]
        self.override=override
        if debug:
            self.generated_files=[]
        if type=="MD":
            pass
        else:
            with open("templates/item","r",encoding="utf-8") as f:
                self.item=f.read()
            with open("templates/html.html","r",encoding="utf-8") as f:
                self.html=f.read()
    def gen_index(self,path):
        gen_ingore=os.path.join(path,"/.genignore")
        if os.path.exists(gen_ingore):
            with open(gen_ingore) as f:
                self.gen_ingore.extend(f.readlines())
        if self.type=="MD":
            self.gen_md(path)
        else:
            if os.path.exists(path+'/static'):
                 shutil.rmtree(path+'/static')
            shutil.copytree('static',path+'/static')
            self.gen_html(path)
    
    def gen_html(self,path,depth=0):
        dirs = os.listdir(path)
        try:
            value = "<h3> Tables of content </h3><br>"
            c_dirs = os.listdir(os.path.join(path))
            print(c_dirs)
            for c_dir in c_dirs:
                c_path = os.path.join(path, c_dir)
                if not os.path.isfile(c_path):
                    ch_dir = c_dir.strip().replace(" ", "%20")
                    value+=self.item.format(icon=f"./{'../'*depth}static/folder.png",href=ch_dir,title=c_dir)
                    #value += f"{'1.' if self.num else '- '}{self.folder_icon if self.icon else ''} [{c_dir}](./{ch_dir})\n"
                    self.gen_html(c_path,depth+1)

                else:
                    if c_dir != "index.html":
                        extension=""
                        parts=c_dir.split(".")
                        if len(parts)>1:
                            extension=parts[-1]
                        ch_dir = c_dir.strip().replace(" ", "%20")
                        if extension in ["java","yaml","yml","py","php"]:
                            content_file=os.path.join(path,".genc/",parts[0]+".md")
                            if not os.path.exists(path+"/.genc"):
                                os.makedirs(path+"/.genc",exist_ok=True)
                            ch_dir = content_file.strip().replace(" ", "%20")
                            with open(content_file,"w",encoding="utf-8") as f:
                                with open(os.path.join(path,c_dir),"r",encoding="utf-8",) as inp:
                                    f.write(f"```{extension}\n{inp.read()}\n```")
                        value+=self.item.format(icon=f"./{'../'*depth}static/file.png",href=ch_dir,title=c_dir)
                        #value += f"{'1.' if self.num else '- '}{self.file_icon if self.icon else ''} [{c_dir}](./{ch_dir})\n"
            readme = os.path.join(path, "index.html")
            print(readme,value)
            if self.override or  (not os.path.exists(readme)):
                with open(readme, "w", encoding='utf-8') as file:
                    content=self.html.replace("{body}",value)
                    content=content.replace("{Title}",path)
                    print(content)
                    if self.debug:
                        self.generated_files.append(content)
                    else:
                        file.write(content)

                    print("Written:\n", value)
        except Exception as e:
            print(e,e, "Missed something or tried to open list readme.md")

    def gen_md(self, path):
        dirs = os.listdir(path)
        try:
            value = "## Tables of content\n"
            c_dirs = os.listdir(os.path.join(path))
            print(c_dirs)
            for c_dir in c_dirs:
                c_path = os.path.join(path, c_dir)
                if not os.path.isfile(c_path):
                    ch_dir = c_dir.strip().replace(" ", "%20")
                    value += f"{'1.' if self.num else '- '}{self.folder_icon if self.icon else ''} [{c_dir}](./{ch_dir})\n"
                    self.gen_md(c_path)

                else:
                    ch_dir = c_dir.strip().replace(" ", "%20")
                    if c_dir != "readme.md":
                        value += f"{'1.' if self.num else '- '}{self.file_icon if self.icon else ''} [{c_dir}](./{ch_dir})\n"
            readme = os.path.join(path, "readme.md")
            print(readme)
            with open(readme, "w", encoding='utf-8') as file:
                file.write(value)
                print("Written:\n", value)
        except Exception as e:
            print(e, "Missed something or tried to open list readme.md")
            traceback.print_exc()


if __name__ == "__main__":
    par = sys.argv[1]
    icon =  True
    num = False 
    folder_icon = '📁'
    file_icon = '📄'
    index_type="HTML"
    over_ride=False
    if (len(sys.argv) >= 3):
        index_type = sys.argv[2].upper() if sys.argv[2] else "HTML"
    if (len(sys.argv) >= 4):
        over_ride = False if sys.argv[3].lower() == "false" else True
    if (len(sys.argv) >= 5):
        icon = False if sys.argv[4].lower() == "false" else True
    if (len(sys.argv) >= 6):
        num = False if sys.argv[5].lower() == "false" else True
    if (len(sys.argv) >= 7):
        folder_icon = sys.argv[6] if sys.argv[6] else '📁'
    if (len(sys.argv) >= 8):
        file_icon = sys.argv[7] if sys.argv[7] else '📄'
    gen = GenIndex(num=num, icon=icon, folder_icon=folder_icon,
                   file_icon=file_icon,type=index_type)
    gen.gen_index(par)
