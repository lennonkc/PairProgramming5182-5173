import os
import sys
import random
# -*- coding: UTF-8 -*-


class Formula:
    '所有算式的基类,表示第几次生成'
    FCount = 0

    def __init__(self,numbers,range):
        Formula.FCount += 1
        'self.numbers 是生成题目总个数, self.range 是数值的范围'
        self.numbers = numbers
        self.range = range

    '这是一个用于生成随机数符号的函数, 1-4 分别代表 + - * // '
    def GenerateOperator(self,numeralNumbers):
        if(numeralNumbers == 2):
            key = [random.randint(1,4)]
        if (numeralNumbers == 3):
            key = [random.randint(1, 4),random.randint(1,4)]
        if (numeralNumbers == 4):
            key = [random.randint(1, 4),random.randint(1,4),random.randint(1,4)]
        return key

    '这是一个将将print值写入到文件中的函数'
    def WriteFile(self,numeralNumbers,stringN,stringO,QN):
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
        if (numeralNumbers == 3):
            print("%d、 %s %s %s %s %s= "% (QN,stringN[0],stringO[0],stringN[1],stringO[1],stringN[1]),file = file )
        if (numeralNumbers == 4):
            print("%d、 %s %s %s %s %s %s %s= "% (QN,stringN[0],stringO[0],stringN[1],stringO[1],stringN[1],stringO[2],stringN[2]),file = file )


    def generate(self,QuestionNumber):
        '这是一个用于生成随机数值的函数'
        OperatorNumbers = random.randint(1,3)
        Rang = self.range                                       #避免不小心修改self.range 所以引入Rang
        if(OperatorNumbers == 1):
            numeral = [random.randint(1,Rang),  random.randint(1,Rang)]
            key = self.GenerateOperator(OperatorNumbers+1)      #OperatorNumbers + 1 = numbers 操作符数 + 1 = 数值数
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


count1 = Formula(5,100)
count1.FormulaNumbers()
