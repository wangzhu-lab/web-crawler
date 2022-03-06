#正则表达式：字符串模式 (判断字符串是否符合一定的标准)

import re
#创建模式对象

pat = re.compile("AA")      #此处的AA，是正则表达式，用来验证其他的字符串
#m = pat.search("CBA")      #search字符串被校验的内容
#m = pat.search("ABCAA")
#m = pat.search("AABCAADDCCAAA")     #search方法，进行比对查找，只找第一个


#没有模式对象
# m = re.search("asd","Aasad")        #前面的字符串是规则(模板)，后面的字符串是被校验的对象
# print(m)


#print(re.findall("a","ASDaDFGAa"))      #前面的字符串是规则(正则表达式)，后面的字符串是被校验的字符串


#print(re.findall("[a-z]","asdASDVC"))


# print(re.findall("[A-Z]+","ASDaDFGAa"))

#sub

print(re.sub("a","A","abcdcasd"))       #找到a用A替换

#建议在正则表达式中，被比较的字符串的前面加r，不用担心转译字符的问题
a = r"\aabd- \ '"
print(a)