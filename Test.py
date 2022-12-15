import GenIndex
gen=GenIndex.GenIndex(num=False,icon=True,type="HTML",debug=False) 
print(gen.html)
print(gen.item)
gen.gen_index("E:/Git Projects/Docker")

