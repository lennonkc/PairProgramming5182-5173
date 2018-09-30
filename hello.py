import re
import random

if __name__ == '__main__':
    str1 = '1+5*(6-1) = 10'
    str2 = '1+5+(6+1) = 20'
    s = re.search('\(...\)',str1).span()
    print(s,str1[4:9],str1[0])

    s = str1.replace(' ','')
    re.search('=',str1).end()
    print(s,s[10:])

    fuhao = re.finditer('[^0-9 =()]',str1)
    for match  in fuhao:
        print(match.group())

    shuzi = re.finditer('[0-9]',str1)
    for match  in shuzi:
        print(match.group())

string = "1. 10*5÷8/3*7 = "
formula = re.sub('[^.()/*÷\-+0-9]', "", string)  # 清除非算式符号  # 清除非算式符号
if(formula[1] == '.'):formula = formula.replace(formula[0:3],'')
print(formula)

X1 = int(random.random()*10000)
print(X1)