import os
import re
import sys
import functools
# -*- coding: UTF-8 -*-
import random

class Formula:
    '所有算式的基类,表示第几次生成'
    FCount = 0

    def __init__(self,numbers,range):
        Formula.FCount += 1
        'self.numbers 是生成题目总个数, self.range 是数值的范围'
        self.numbers = numbers
        self.range = range

    def GenerateOperator(self,numeralNumbers):
        '这是一个用于生成随机数符号的函数, 1-4 分别代表 + - * // '
        if(numeralNumbers == 2):
            key = [random.randint(1,4)]
        if (numeralNumbers == 3):
            key = [random.randint(1, 4),random.randint(1,4)]
        if (numeralNumbers == 4):
            key = [random.randint(1, 4),random.randint(1,4),random.randint(1,4)]
        return key

    def WriteFile(self,numeralNumbers,stringN,stringO,QN):
        '这是一个将将print值写入到文件中的函数'
        file = open("./Exercises.txt",'a+')
        'i 以及 下面的 for 循环帮助1-4转换成 +-*/ '
        i = 0
        for chars in stringO:
            if(chars == 1):
                stringO[i] = '+'
            if (chars == 2):
                stringO[i] = '-'
            if (chars == 3):
                stringO[i] = '*'
            if (chars == 4):
                stringO[i] = '/'
            i += 1
        if (numeralNumbers == 2):
            print("%d、 %s %s %s = "% (QN,stringN[0],stringO[0],stringN[1]),file = file )
            file.close()
        if (numeralNumbers == 3):
            print("%d、 %s %s %s %s %s= "% (QN,stringN[0],stringO[0],stringN[1],stringO[1],stringN[1]),file = file )
            file.close()
        if (numeralNumbers == 4):
            print("%d、 %s %s %s %s %s %s %s= "% (QN,stringN[0],stringO[0],stringN[1],stringO[1],stringN[1],stringO[2],stringN[2]),file = file )
            file.close()

    def generate(self,QuestionNumber):
        '这是一个用于生成随机数值的函数'
        OperatorNumbers = random.randint(1,3)
        Rang = self.range                                       #避免不小心修改self.range 所以引入Rang
        if(OperatorNumbers == 1):
            numeral = [random.randint(1,Rang),  random.randint(1,Rang)]
            key = self.GenerateOperator(OperatorNumbers+1)      #OperatorNumbers + 1 = numbers 操作符数 + 1 = 数值数
            while(key[0] == 2 and (numeral[0]<numeral[1])):     #一个运算符时的非负数判断
                numeral = [random.randint(1,Rang),  random.randint(1,Rang)]
            self.WriteFile(OperatorNumbers+1,numeral,key,QuestionNumber)
        if (OperatorNumbers == 2):
            numeral = [ random.randint(1,Rang),  random.randint(1,Rang), random.randint(1,Rang)]
            key = self.GenerateOperator(OperatorNumbers + 1)
            self.WriteFile(OperatorNumbers + 1, numeral, key,QuestionNumber)
        if (OperatorNumbers == 3):
            numeral = [random.randint(1,Rang),  random.randint(1,Rang), random.randint(1,Rang),  random.randint(1,Rang)]
            key = self.GenerateOperator(OperatorNumbers + 1)
            self.WriteFile(OperatorNumbers + 1, numeral, key,QuestionNumber)

    def FormulaNumbers(self):
        '这是一个依次生成多条算式的函数,生成self.numbers 条算式'
        if(self.numbers == 0):
            print("请正确输入生成题目的个数")
        if(self.numbers != 0):
            test = self.numbers
            QuestionNumber = 1
            while(test != 0):
                self.generate(QuestionNumber)
                test -= 1
                QuestionNumber += 1

class ANSWERS:
    def __init__(self,ANSfile):
        self.ANSfile = ANSfile

    def mul_divOperation(self, s):
        sub_str = re.search('(\d+\.?\d*[*/]-?\d+\.?\d*)', s)
        while sub_str:
            sub_str = sub_str.group()
            if sub_str.count('*'):
                l_num, r_num = sub_str.split('*')
                s = s.replace(sub_str, str(float(l_num) * float(r_num)))
            else:
                l_num, r_num = sub_str.split('/')
                s = s.replace(sub_str, str(float(l_num) / float(r_num)))
            sub_str = re.search('(\d+\.?\d*[*/]\d+\.?\d*)', s)
        return s

    def add_minusOperation(self, s):
        s = '+' + s
        tmp = re.findall('[+\-]\d+\.?\d*', s)
        s = str(functools.reduce(lambda x, y: float(x) + float(y), tmp))
        return s

    def compute(self, formula):
        "计算中的辅助函数"
        formula = self.mul_divOperation(formula)
        formula = self.add_minusOperation(formula)
        return formula

    def Transfer(self, formula):
        '这是一个把小数字符串转换成分数的函数'
        i = formula.find('.')
        if (i != -1):  # 如果存在小数点，只取小数点后三位
            e = float(formula[0:i + 4])
            intE = int(e)
            term = round(e - intE, 4)  # 小数部分四舍五入
            if (term == 0): return formula[:i]
            termD = term * 1000
            Deno = 1000
            while (termD != Deno):  # 求最大公约数以化简
                if (Deno > termD): Deno = Deno - termD
                if (termD > Deno): termD = termD - Deno
            term = int(term * 1000 / termD)
            Deno = int(1000 / termD)
            if (intE != 0): answers = [str(intE), '’', str(term), '/', str(Deno)]
            if (intE == 0): answers = [str(term), '/', str(Deno)]
            answers = ''.join(answers)
            return answers
        else:
            return formula

    def clearFile(self, filename):
        file = open(filename, "r+")
        string = file.read()
        file.close()  # 读取string后关闭文件，避免误操作
        string = string.replace('、', '')
        string = string.replace('=', '')
        string = string.replace(' ', '')
        return string

    def Answers(self, filename):
        context = self.clearFile(filename)
        i = 0
        formulaNumbers = context.count('\n')  # 统计题目个数
        out = [1] * formulaNumbers  # 生成指定长度的list
        for line in context.splitlines():
            line = line[1:]
            out[i] = self.Transfer(self.compute(line))
            i += 1
        out = '\n'.join(out)
        print(out)
        return out

count1 = Formula(5,100)
count1.FormulaNumbers()
ANS = ANSWERS('Exercises.txt')
ANS.Answers("Exercises.txt")