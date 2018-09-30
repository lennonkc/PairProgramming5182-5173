import re
import functools
# -*- coding: UTF-8 -*-
import random
from optparse import OptionParser

usage = "[<-n> + 数字] 确定题目条数 [<-r> + 数字] 确定数字范围 \n 可选参数: \n <-u> 生成有负数出现的题目 \n [<-a> + (filename)] 回答filename文件的题目 \n [<-j> + (filename)] 批改filename文件的题目"
parser = OptionParser(usage)
parser.print_help()
parser.add_option("-n", action='store', type='int', dest='Numbers', help="生成Numbers条无负数结果的算式,输出文件是StandExercises.txt")
parser.add_option("-r", action='store', type='int', dest='Range', help="指定数字Range范围")
parser.add_option("-u", action='store', type='string', dest='ProExFile', help="生成Numbers条有负数结果的算式,输出文件时Exercises.txt")
parser.add_option("-a", action='store', type='string', dest='AnsFile', help="指定题目文件,并生成答案到Answers.txt")
parser.add_option("-j", action='store', type='string', dest='JudgeFile', help="指定用户答案文件,并将其和标准Answers.txt对比")
options, args = parser.parse_args()


class Genera:

    def __init__(self, numbers, range):
        'self.numbers 是生成题目总个数, self.range 是数值的范围'
        self.numbers = numbers
        self.range = range
        self.filename = 'Exercises.txt'
        self.Fomulas()

    def GeneralOneFormula(self):
        Range = self.range
        # OperateNumbers = random.randint(1, 3)
        X1 = int(random.random() * 10000)
        X2 = int(random.random() * 10000)
        OperateNumbers = X1 % 3 + 1
        CountNUmbers = OperateNumbers + 1
        Ostyle = ['+', '-', '*', '÷']

        # 生成符号list
        Operates = []
        a = 0
        while (a <= OperateNumbers):
            # Operates.append(random.choice(Ostyle))
            if (a == 0):
                Operates.append(Ostyle[X1 % 4])
            if (a == 1):
                Operates.append(Ostyle[X2 % 4])
            if (a == 2):
                Operates.append(Ostyle[(X1 + X2) % 4])
            a += 1
        # 生成数字list与括号list
        Counts = []
        i = CountNUmbers
        while (i > 0):
            X = int(random.random() * 10000) % Range + 1
            if (X % 10 != 1):
                term = str(X)
                Counts.append(term)
            else:
                term = [str(X), '/', str(int(random.random() * 10000) % Range + 1)]
                termT = ''.join(term)
                # 此处插入分数化简
                Counts.append(termT)
            i -= 1
        if ((Operates.count('-') != 0) and (Operates.count('+') != 0) and (
                int(random.random() * 10000) % 7 == 1)):  # 假定1/7的括号生成概率
            leftPosition = int(random.random() * 10000) % OperateNumbers
            rightPosition = random.randint(leftPosition + 2, OperateNumbers + 1) - 1
            # rightPosition = int(random.random() * 10000) % OperateNumbers + 1
            term = '(' + str(Counts[leftPosition])
            Counts[leftPosition] = term
            term = str(Counts[rightPosition]) + ')'
            Counts[rightPosition] = term
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
        return FinalList

    def Fomulas(self):
        Range = self.range
        Numbers = self.numbers
        ' 生成多个Formula并写入文档 '
        file = open("Exercises.txt", 'a+')
        out = ""
        for i in range(1, Numbers + 1):
            out = out + self.GeneralOneFormula() + '\n'
        print(out, file=file)
        file.close()


class Answer:
    '这是用于生成任何题目文件的结果到Answers.txt中的类'

    def __init__(self, FileName):
        self.file = FileName
        self.OpenAFile()

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
        formula = self.mul_divOperation(formula)
        formula = self.add_minusOperation(formula)
        return formula

    def calc(self, formula):
        """计算程序入口"""
        if (formula[0] == '(' and formula[len(formula) - 1] == ')'):
            formula = formula.replace('(', '')
            formula = formula.replace(')', '')
        formula = re.sub('[^.()/*÷\-+0-9]', "", formula)  # 清除非算式符号
        if (formula[1] == '.'):
            formula = formula.replace(formula[0:2], '')  # 计算含有题目序列号的标准算式
        has_parenthesise = formula.count('(')
        while has_parenthesise:
            sub_parenthesise = re.search('\([^()]*\)', formula)  # 匹配最内层括号
            if sub_parenthesise:
                formula = formula.replace(sub_parenthesise.group(), self.compute(sub_parenthesise.group()[1:-1]))
            else:
                has_parenthesise = False
        ret = self.compute(formula)
        return ret

    def Transfer(self, formula):
        '这是一个把小数字符串转换成分数的函数'
        i = formula.find('.')
        if (i != -1 and formula.find('-') == -1):  # 如果存在小数点，只取小数点后三位
            e = float(formula[0:i + 4])
            intE = int(e)
            term = round(e - intE, 4)  # 小数部分四舍五入
            if (term == 0): return formula[:i]
            termD = term * 1000
            Deno = 1000
            if (termD % 333 == 0): Deno = 999  # 优化小学生算术题中常出现的1/3
            while (termD != Deno):  # 求最大公约数以化简
                if (Deno > termD): Deno = Deno - termD
                if (termD > Deno): termD = termD - Deno
            term = int(term * 1000 / termD)
            Deno = int(1000 / termD)
            if (intE != 0): answers = [str(intE), '\'', str(term), '/', str(Deno)]
            if (intE == 0): answers = [str(term), '/', str(Deno)]
            answers = ''.join(answers)
            return answers
        else:
            return formula

    def OpenAFile(self):
        fileE = open(self.file, "r+")
        string = fileE.read()
        fileE.close()
        string = string.replace('÷', '/')
        out = ""
        for line in string.splitlines():
            # out = out + self.compute(line) + '\n'
            out = out.replace('+', '')
            out = out + self.Transfer(self.calc(line)) + '\n'
        fileA = open("Answers.txt", "w+")
        print(out, file=fileA)
        fileA.close()


class Verify:
    '这是一个用于修正有负数结果的式子，判断式子是否有重复，以及生成题目序号的类,判断/后面有没有0'

    # 筛选出等式中的符号
    def __init__(self, FileName):
        self.file = FileName
        self.VerifyAFile()

    def VerifyAFile(self):
        No = 1
        with open(self.file) as r:
            lines = r.readlines()
        with open('StandExercises.txt', 'w') as w:
            for l in lines:
                s = l
                s = s.replace('÷', '/')
                if ((self.math_compute(s) == 1)):
                    position = re.search('\Z', l).end()
                    l = l.replace(l[position - 1], ' = \n')
                    l = str(No) + '. ' + l
                    w.write(l)
                    No += 1
        r.close()
        w.close()

    def filt_sym(self, e1_fs):
        sym_get = ""
        for sym in e1_fs:
            if sym == '+' or sym == '-' or sym == '*' or sym == '/':
                sym_get = sym_get + sym
        return sym_get

    # 筛选出等式中的数字
    def filt_num(self, e1_fn):
        num_get = []
        num_c = ""
        for num in e1_fn:
            if num != '+' and num != '-' and num != '*' and num != '/':
                flag = 1
                num_c += num
            else:
                flag = 0
            if flag == 0:
                num_get = num_get + [float(num_c)]
                num_c = ""
        num_get = num_get + [float(num_c)]
        return num_get

    # 判断优先级
    def judge_pri(self, sym_int):
        i = 0
        sym_p = []
        for sym_jp in sym_int:
            if sym_jp == '/':
                sym_p += [40 + i]
                i += 1
            elif sym_jp == '*':
                sym_p += [30 + i]
                i += 1
            else:
                i += 1
        i = 0
        for sym_jp in sym_int:
            if sym_jp == '-':
                sym_p += [20 + i]
                i += 1
            elif sym_jp == '+':
                sym_p += [10 + i]
                i += 1
            else:
                i += 1
        return sym_p

    # 等式运算计算细节实现
    def int_compute(self, num_int, sym_int):
        sym_p_int = self.judge_pri(sym_int)
        while sym_p_int != []:
            sym = int(sym_p_int[0])
            if sym >= 40:
                if num_int[sym - 40 + 1] == 0:
                    return -1
                num_int[sym - 40] /= num_int[sym - 40 + 1]
                num = num_int[sym - 40: sym - 40 + 1]
                del num_int[sym - 40 + 1: sym - 40 + 2]
                sym_int = sym_int[:sym - 40] + sym_int[sym - 40 + 1:]
            elif sym >= 30:
                num_int[sym - 30] *= num_int[sym - 30 + 1]
                num = num_int[sym - 30: sym - 30 + 1]
                del num_int[sym - 30 + 1: sym - 30 + 2]
                sym_int = sym_int[:sym - 30] + sym_int[sym - 30 + 1:]
            elif sym >= 20:
                num_int[sym - 20] -= num_int[sym - 20 + 1]
                num = num_int[sym - 20: sym - 20 + 1]
                if num[0] < 0:
                    return -1
                del num_int[sym - 20 + 1: sym - 20 + 2]
                sym_int = sym_int[:sym - 20] + sym_int[sym - 20 + 1:]
            elif sym >= 10:
                num_int[sym - 10] += num_int[sym - 10 + 1]
                num = num_int[sym - 10: sym - 10 + 1]
                del num_int[sym - 10 + 1: sym - 10 + 2]
                sym_int = sym_int[:sym - 10] + sym_int[sym - 10 + 1:]
            sym_p_int = self.judge_pri(sym_int)
        return float(num[0])

    # 等式运算
    def compute_c(self, e1):
        num_int = float()
        num_int = self.filt_num(e1)
        sym_int = self.filt_sym(e1)
        flag = self.int_compute(num_int, sym_int)
        if flag < 0:
            return 'f'
        else:
            return str(flag)

    # 将等式中括号里面的等式提取出来
    def judge_bracket(self, equ_j):
        left = equ_j.rfind('(')
        right = equ_j.find(')', left)
        e1 = equ_j[left + 1:right]
        c1 = self.compute_c(e1)
        if c1 == 'f':
            return False
        equ_j = equ_j[0:left] + str(c1) + equ_j[(left + len(c1)):]
        equ_j = equ_j[0: left + len(str(c1))] + equ_j[right + 1:]
        return equ_j

    def math_compute(self, equation):
        equ_m = equation
        while equ_m.find('(') != -1:
            if equ_m.find('(') != -1:
                equ_m = self.judge_bracket(equ_m)
                if not equ_m:
                    break;
            else:
                break
        if not equ_m:
            return 0
        elif equ_m.find('+') != -1 or equ_m.find('-') != -1 or equ_m.find('*') != -1 or equ_m.find('/') != -1:
            val = self.compute_c(equ_m)
            if val == 'f':
                return 0
            else:
                return 1
        else:
            return 1


class Judge:
    '判断Exercises 和 Answers.txt ，并返回处理结果'

    def __init__(self, FileName, FilenameAns):
        self.user_file = FileName
        self.standAns_file = FilenameAns
        self.judge_ans(self.user_file, self.standAns_file)

    def judge_ans(self, user_ans, stand_ans):
        user_a = open(user_ans, 'r')
        std_a = open(stand_ans, 'r')
        i = 0
        c_sum = []
        e_sum = []
        while 1:
            equa_u = user_a.readline()
            equa_s = std_a.readline()
            if not equa_u:
                break
            ind = equa_u.rfind('=')
            if equa_u[ind + 1:].strip() == equa_s.strip():
                i += 1
                c_sum += [i]
            else:
                i += 1
                e_sum += [i]
        print("Correct: ", len(c_sum), c_sum)
        print("Wrong: ", len(e_sum), e_sum)


if options.Numbers and options.Range and options.ProExFile:
    '生成Numbers条有负数结果的算式, 再将其标准化(去除中间过程有负数结果的算式以及/后面有0的非法算式), 输出文件是StandExercises.txt'
    fileE = Genera(options.Numbers, options.Range)
    fileStand = Verify(fileE.filename)

if options.Numbers and options.Range and options.ProExFile and options.AnsFile:
    '生成Numbers条有负数结果的算式, 再将其标准化(去除中间过程有负数结果的算式以及/后面有0的非法算式), 输出文件是StandExercises.txt'
    fileE = Genera(options.Numbers, options.Range)
    fileStand = Verify(fileE.filename)
    fileA = Answer(options.AnsFile)

if options.AnsFile and not options.Numbers:
    '回答-a后面的filename题目文件,并输出结果到Answers.txt文件'
    fileA = Answer(options.AnsFile)

if options.ProExFile and options.Numbers and options.Range and not options.AnsFile:
    '生成Numbers条有负数结果的算式, 生成文件是Exercises.txt'
    fileE = Genera(options.Numbers, options.Range)

if options.JudgeFile and not options.Numbers and not options.Range and not options.ProExFile:
    '-j 接一个用户的答案文件, 并将其和标准答案文件Answers.txt比较'
    FileA = Judge(options.JudgeFile, "Answers.txt")
