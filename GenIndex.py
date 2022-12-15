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
    def __init__(self, num=False, icon=False, folder_icon='📁', file_icon='📄', type="MD",debug=False):
        self.num = num
        self.icon = icon
        self.folder_icon = folder_icon
        self.folder_icon = file_icon
        self.type = type
        self.debug=debug
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
        if self.type=="MD":
            self.gen_md(path)
        else:
            shutil.copy('static',path+'/static')
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
                    ch_dir = c_dir.strip().replace(" ", "%20")
                    if c_dir != "index.html":
                        value+=self.item.format(icon=f"./{'../'*depth}static/file.png",href=ch_dir,title=c_dir)
                        #value += f"{'1.' if self.num else '- '}{self.file_icon if self.icon else ''} [{c_dir}](./{ch_dir})\n"
            readme = os.path.join(path, "index.html")
            print(readme,value)
            with open(readme, "w", encoding='utf-8') as file:
                content=self.html.replace("{body}",value)
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
    icon = False if sys.argv[2].lower() == "false" else True
    num = False if sys.argv[3].lower() == "false" else True
    folder_icon = '📁'
    file_icon = '📄'
    if (len(sys.argv) >= 5):
        folder_icon = sys.argv[4] if sys.argv[4] else '📁'
    if (len(sys.argv) >= 6):
        file_icon = sys.argv[5] if sys.argv[5] else '📄'
    gen = GenIndex(num=num, icon=icon, folder_icon=folder_icon,
                   file_icon=file_icon)
    gen.gen_index(par)
