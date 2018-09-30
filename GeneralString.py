# coding utf-8
import os
import sys
import random
import re
import functools


def generalString():
    # 定义变量
    Range = 100
    OperateNumbers = random.randint(1, 3)
    CountNUmbers = OperateNumbers + 1
    Ostyle = ['+', '-', '*', '÷']
    OperateStyle = random.choice(Ostyle)
    # Cstyle = ['分数', '整数', '整数', '整数', '整数']  # 降低生成分数的概率
    # CountStyle = random.choice(Cstyle)

    # 生成符号list
    Operates = []
    for a in range(OperateNumbers):
        Operates.append(random.choice(Ostyle))
    print(Operates)

    # 生成数字list与括号list
    Counts = []
    # print(CountNUmbers)
    i = CountNUmbers
    while (i > 0):
        if (random.randint(1,10) != 1 ):
            term = str(random.randint(1, Range))
            Counts.append(term)
        else:
            term = [str(random.randint(1, Range)), '/', str(random.randint(1, Range))]
            termT = ''.join(term)
            # 此处插入分数化简
            Counts.append(termT)
        i -= 1
    if (random.randint(1, 6) == 1):  # 假定1/6的括号生成概率
        leftPosition = random.randint(1, OperateNumbers) - 1
        rightPosition = random.randint(leftPosition + 2, OperateNumbers + 1) - 1
        term = '(' + str(Counts[leftPosition])
        Counts[leftPosition] = term
        term = str(Counts[rightPosition]) + ')'
        Counts[rightPosition] = term
    print(Counts)

    # 合并符号list 数字括号list
    FinalList = []
    j = 0
    k = 0
    i = OperateNumbers + CountNUmbers - 1
    while (i >= 0):
        if (i % 2 != 1):
            FinalList.append(Counts[j])
            j += 1
        else:
            FinalList.append(Operates[k])
            k += 1
        i -= 1
    FinalList = ''.join(FinalList)
    print(FinalList)
    print(FinalList.find('-'))


generalString()
