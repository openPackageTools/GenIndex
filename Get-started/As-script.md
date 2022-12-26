# Getting started with GenIndex as script
   
   Here we take a quick overview about how to use GenIdex as script 📃.
   
1. Clone the git repo into your system.

   ```shell
   git clone https://github.com/openPackageTools/GenIndex.git
   ```
   or download ⬇ repo as zip file
   
   ![Screenshot 2022-12-26 004604](https://user-images.githubusercontent.com/61611561/209479740-8d6362e2-eaa3-4cec-be32-3bde5baf884f.png)
   
2. Navigate to GenIndex directory.
  
   ```shell
   cd GenIndex
   ```
 
3. Run python script by path to directory (repo or site) for which we are generating pages.

  ```shell
  ./GenIndex  path_to_repo_or_site
  ```

4. Check the directory and open 🔧 index.html. You will may face some difficulty navigating between pages if you observing pages on local machine.
   After deployment to github pages these issues will be fixed.
6. Yeah! 🥳, We just generated.

```
Note: If you already have a index.html file your dir them you don't see any changes because by default GenIndex didn't override existing file to
avoid acidental deletion of you site😬
```

## What's next

- Read detailed overview of available options [here](./detailed-overview.md)
