# Get Started with GenIndex
  
  Here we take a qwik overview how to get started with GenIndex. It can be accomplished with following steps.

1. Clone the git repo into your system.

   ```shell
   git clone https://github.com/openPackageTools/GenIndex.git
   ```
   or download repo as zip file
   
   ![Screenshot 2022-12-26 004604](https://user-images.githubusercontent.com/61611561/209479740-8d6362e2-eaa3-4cec-be32-3bde5baf884f.png)

2. Create python file and import GenIndex module

   ```python
   import GenIndex
   ```
   You can also import GenIndex class directly
   
    ```python
    from GenIndex import GenIndex
    ```
   For this guide we will follow first approch

3. Create an object of GenIndex class. There are many options to customize the object but we use default for now. Default option generates Html pages with default 
   card items.
 
   ```python
   import GenIndex
   gen = GenIndex.GenIndex()
   ```
 
4. Call `gen_index(root_dir)` method with path to root directory as argument.
   
   ```python
   import GenIndex
   gen = GenIndex.GenIndex()
   gen.gen_index("./site/tutorials")
   ```
5. Check the directory you provided and open index.html file inside that.
5. Yeah! 🥳 you did it 🙌.
``` 
Note: If you already have a index.html file your dir them you don't see any changes because by default GenIndex didn't override existing file to
avoid acidental deletion of you site😬
```
