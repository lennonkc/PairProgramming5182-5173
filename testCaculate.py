# coding utf-8
import os
import sys
import random
import re
import functools


def mul_divOperation(s):
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


def add_minusOperation(s):
    s = '+' + s
    tmp = re.findall('[+\-]\d+\.?\d*', s)
    s = str(functools.reduce(lambda x, y: float(x) + float(y), tmp))
    return s


def Transfer(formula):
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


def compute(formula):
    formula = mul_divOperation(formula)
    formula = add_minusOperation(formula)
    # formula = Transfer(formula)
    return formula


def clearFile(filename):
    file = open(filename, "r+")
    string = file.read()
    file.close()  # 读取string后关闭文件，避免误操作
    string = string.replace('、', '')
    string = string.replace('=', '')
    string = string.replace(' ', '')
    return string


def Answers(filename):
    context = clearFile(filename)
    i = 0
    formulaNumbers = context.count('\n')  # 统计题目个数
    out = [1] * formulaNumbers  # 生成指定长度的list
    for line in context.splitlines():
        line = line[1:]
        out[i] = Transfer(compute(line))
        i += 1
    out = '\n'.join(out)
    return out


# str1 = '4+9/7'
# print(compute(str1))

"""
str1 = '4.0'
str2 = '489'
Transfer(str2)
print(Transfer(str1))

"""
file = 'Exercises.txt'
e = Answers(file)
fileA = open("Answers.txt", 'w+')
print("%s" % e, file=fileA)
fileA.close()

# Answers(file)
# e = Answers(file)
# e = float(e[0:6])
# compute(line)
