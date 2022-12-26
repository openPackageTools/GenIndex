"""
 This module generates indices for github pages. Github repo which false in category of code base more than a static site and
 we try to deploy such files to github pages then for nested folder either we have to create a index.html or a readme to access these code
 bases. This Module help this this particular case.

Classes:

   - GenIndex - Configures and generates the index pages.
  
 
"""
import traceback
import shutil
import os
import sys
# Path ./DSA-Bootcamp-Java/lectures/


class GenIndex:
    """Class to handle all configuration and to generate The index files

     ...

     Attributes
     ----------
     Common:
        parent_dir : str
            path to the parent directory of site or repo 
        type : str
            Type of the index file to be generated. This can be HTML and MD(Markdown).Default is HTML.
        override : bool
            Whether to override or not an existing index file of specified type
        debug : bool
            Flag to run code in debug mode. In Debug mode add content to be written in index files in genarated_files list.
            Which can be observed to get inside.
        genarated_files : list
            contains content to be written to file in debug mode.
        gen_ignore : list
            contains list of files to be excluded in generated index pages. It also consider .gitignore and .geignore to
            it's content.

     Type specific attrs:
        HTML attrs:
            item_type : str
                Specifies the type of item used for each dir or file when type is HTML. It can be LIST or CARD. Default value is LIST.

        MD attrs:
            num : bool
                Flag to tell wether to show a numeric list for item list.
            icon : bool
                Flag to tell wether to show icon. Icon are some text or emojis shown in the start of item.
            folder_icon : str
                Text or emojis to be shown before each item list whose type is a file.
            file_icon : str     
                Text or emojis to be shown before each item list whose type is a folder.


     Methods
     -------
     gen_index(path) -> None
         Configures the gen_ignore files from root of repo or site. Coppies resource to repo and calls subsequent method according
         to type of index.
     add_ignored_item(file) -> None
         Adds item to gen_ignore list from specified file.
     gen_html(path,depth=0) -> None
         Generates HTML index pages.
     gen_md(path) -> None
         Generates MD index pages.
     write_to_md_file(path,file,value) -> None
          Write generated code for md index pages to md files.
     write_to_html_file(path,file,value):
          Write generated code for HTML index pages to HTML files.
     check_presence(self,file) -> 
          check for presence of a file in excluded files and folders.


    """

    def __init__(self, override=False, item_type="LIST", num=False, icon=False, folder_icon='📁', 
           file_icon='📄', type="HTML", debug=False,item_template="templates/item", page_template="templates/basic.html"
    ):
        """Set up all configuration parameter

         Parameters
         ----
        Common:
            type : str
                Type of the index file to be generated. This can be HTML and MD(Markdown).Default is HTML.
            override : bool
                Whether to override or not an existing index file of specified type
            debug : bool
                Flag to run code in debug mode. In Debug mode add content to be written in index files in genarated_files list.
                Which can be observed to get inside.

        Type specific attrs:
            HTML attrs:
                item_type : str
                    Specifies the type of item used for each dir or file when type is HTML. It can be LIST or CARD. Default value is LIST.

            MD attrs:
                num : bool
                    Flag to tell wether to show a numeric list for item list.
                icon : bool
                    Flag to tell wether to show icon. Icon are some text or emojis shown in the start of item.
                folder_icon : str
                    Text or emojis to be shown before each item list whose type is a file.
                file_icon : str     
                    Text or emojis to be shown before each item list whose type is a folder.



        """
        self.num = num
        self.icon = icon
        self.folder_icon = folder_icon
        self.file_icon = file_icon
        self.type = type
        self.item_template = item_template
        self.page_template = page_template
        self.item_type = item_type
        self.debug = debug
        self.gen_ingore = []
        self.override = override
        if debug:
            self.generated_files = []
        if type == "MD":
            pass
        else:
            with open(self.item_template, "r", encoding="utf-8") as f:
                self.item = f.read()
            if self.item_type == "CARD":
                self.page_template = "templates/card.html"
            with open(self.page_template, "r", encoding="utf-8") as f:
                    self.html = f.read()
            print("Using",self.item_template,"as Item template...")
            print("Using",self.page_template,"as page template...")

    def gen_index(self, path):
        """
        Configures repo or site directory for resources

        """
        self.parent_dir = path
        self.add_ignored_item(os.path.join(path, "/.genignore"))
        self.add_ignored_item(os.path.join(path, "/.gitignore"))
        self.gen_ingore.append("genc")
        self.gen_ingore.append("genstatic")
        if self.type == "MD":
            self.gen_md(path)
        else:
            if os.path.exists(path+'/genstatic'):
                shutil.rmtree(path+'/genstatic')
            shutil.copytree('genstatic', path+'/genstatic')
            self.gen_html(path)

    def add_ignored_item(self, file):
        """
        Add ignore files to excluded list.

        This method goes throught the list of files in provided file to add them in excluded list.
        
        """
        if os.path.exists(file):
            with open(file) as f:
                self.gen_ingore.extend(f.readlines())

    def check_presence(self, file):
        """
        Checks if a file is excluded or not

        Parameter
        ---------
        file -> str
            file to be checked for presence
        """
        import re
        for item in self.gen_ingore:
            i = item.split("/")[-1]
            if re.match(i, file):
                return True
        return False

    def gen_html(self, path, depth=0):
        """ Generates html index pages

        Recursively goes throught all directory and add index file in them.

        Parameters:
        path -> str
            path of current directory
        depth -> str
            Depth is used to measure depth of current directory from root directory. It help to build path to refer to static
            resources added to repo or site root directory. 
        """
        dirs = os.listdir(path)
        try:
            value = ""
            c_dirs = os.listdir(os.path.join(path))
            for c_dir in c_dirs:
                if self.check_presence(c_dir):
                    continue
                c_path = os.path.join(path, c_dir)
                if not os.path.isfile(c_path):
                    ch_dir = c_dir.strip().replace(" ", "%20")
                    value += self.item.format(
                        icon=f"./{'../'*depth}genstatic/folder.png", href=ch_dir, title=c_dir)
                    #value += f"{'1.' if self.num else '- '}{self.folder_icon if self.icon else ''} [{c_dir}](./{ch_dir})\n"
                    self.gen_html(c_path, depth+1)

                else:
                    if c_dir != "index.html":
                        extension = ""
                        parts = c_dir.split(".")
                        if len(parts) > 1:
                            extension = parts[-1]
                        ch_dir = c_dir.strip().replace(" ", "%20")
                        if extension in ["java", "yaml", "yml", "py", "php","sh","html","css","js"]:
                            content_file = os.path.join("genc", parts[0]+".md")
                            content_path = os.path.join(path, content_file)
                            genc_path = os.path.join(path, "genc")
                            if not os.path.exists(genc_path):
                                os.makedirs(genc_path, exist_ok=True)
                            ch_dir = os.path.join(
                                "genc", parts[0]).strip().replace(" ", "%20")
                            with open(content_path, "w", encoding="utf-8") as f:
                                with open(os.path.join(path, c_dir), "r", encoding="utf-8",) as inp:
                                    file_content = inp.read()
                                    f.write(
                                        f"```{extension}\n{file_content}\n```")
                        if extension =="md":
                            ch_dir=parts[0].strip().replace(" ", "%20")
                        value += self.item.format(
                            icon=f"./{'../'*depth}genstatic/file.png", href=ch_dir, title=c_dir)
                        #value += f"{'1.' if self.num else '- '}{self.file_icon if self.icon else ''} [{c_dir}](./{ch_dir})\n"
            readme = os.path.join(path, "index.html")
            self.write_to_html_file(path, readme, value, depth)
        except Exception as e:
            print(e, e, "Missed something or tried to open list readme.md")

    def gen_md(self, path):
        """Generates Markdown index pages

        Recursively goes throught all directory and add readme file in them.

        Parameters:
        path -> str
            path of current directory
        
        """
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
            self.write_to_md_file(path, readme, value)

        except Exception as e:
            print(e, "Missed something or tried to open list readme.md")
            traceback.print_exc()

    def write_to_md_file(self, path, file, value):
        """
        Write index content to a index file
    
        Parameter
        --------
        path -> str
            path of file
        file -> str
            file to which the content to be written
        value -> str
            value to be written in file
        """

        if self.override or (not os.path.exists(file)):
            with open(file, "w", encoding='utf-8') as f:
                f.write(value)
                print("Written:\n", value)

    def write_to_html_file(self, path, file, value, depth):
        """
        Write index content to a index file
    
        Parameter
        --------
        path -> str
            path of file
        file -> str
            file to which the content to be written
        value -> str
            value to be written in file
        """
        if self.override or (not os.path.exists(file)):
            with open(file, "w", encoding='utf-8') as f:
                content = self.html.replace("{body}", value)
                content = content.replace(
                    "{Title}", path.replace(self.parent_dir, ""))
                content = content.replace(
                    "{content_title}", "Table of content")
                content = content.replace(
                    "{root}", "../"*depth)
                if self.debug:
                    self.generated_files.append(content)
                else:
                    f.write(content)
                    f.close()
                    print("Generated:", path, file)

# Driver code for module
if __name__ == "__main__":
    par = sys.argv[1]
    icon = True
    num = False
    folder_icon = '📁'
    file_icon = '📄'
    index_type = "HTML"
    item_type = "LIST"
    over_ride = False
    item_template="templates/item"
    page_template="templates/basic.html"
    if (len(sys.argv) >= 3):
        over_ride = False if sys.argv[2].upper() == "FALSE" else True
    if (len(sys.argv) >= 4):
        index_type = sys.argv[3].upper() if sys.argv[3] else "HTML"
    if index_type == "MD":
        if (len(sys.argv) >= 5):
            icon = False if sys.argv[4].upper() == "FALSE" else True
        if (len(sys.argv) >= 6):
            num = False if sys.argv[5].upper() == "FALSE" else True
        if (len(sys.argv) >= 7):
            folder_icon = sys.argv[6] if sys.argv[6] else '📁'
        if (len(sys.argv) >= 8):
            file_icon = sys.argv[7] if sys.argv[7] else '📄'
    elif index_type == "HTML":
        if (len(sys.argv) >= 5):
            item_type = sys.argv[4].upper()
            print(item_type)
        if item_type == "CUSTOM":
            if (len(sys.argv) >= 6):
                item_template = sys.argv[5]
            if (len(sys.argv) >= 7):
                page_template = sys.argv[6]
    else:
        print("Ivalid index type")
        exit()
    if over_ride:
        print("Warning: It will make destructive changes,Do you want to continue(Y/N) ?")
        if input().lower() == "n":
            exit()
    gen = GenIndex(num=num, icon=icon, folder_icon=folder_icon,
                   file_icon=file_icon, type=index_type, override=over_ride, item_type=item_type,
                   item_template=item_template,page_template=page_template)
    gen.gen_index(par)
