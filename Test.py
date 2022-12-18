import GenIndex
gen=GenIndex.GenIndex(num=False,icon=True,type="HTML",debug=False) 
print(gen.html)
print(gen.item)
#TEST for GenIndex
gen.gen_index("E:/Git Projects/Docker")

