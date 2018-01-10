# вот здесь вам нужно сделать исполнитель
# на вход он получит список
# например,
# [('a', 'ID'), ('b', 'ID'), ('num', 'RESERVED'), ('a', 'ID'), ('3', 'INT'), ('<', 'RESERVED'), ('tag1', 11), ('jf', 'RESERVED'), ('b', 'ID'), ('4', 'INT'), (':=', 'RESERVED')]
# первые три это объявления переменных. 
# с 4 по 8 начало условия.
# ('tag1', 11) -- это то куда нужно перейти в польской строке, если ложно
# ('b', 'ID'), ('4', 'INT'), (':=', 'RESERVED')
# переменной b присваивается зачение четыре 
# и далее как это обычно происходит в обратной полськой строке
# здесь [('a', 'ID')] -- это имя переменной при обявлении нужно следить,
# что это простая переменная -- num
# массив -- arr
# двумерный массив -- mtx

# здесь нужно подумать я не до конца уверен, но можно
# сделать так
# хранение переменных в словарях 
# пример для обыковенных переменных
# variables = {'var_name': 4, 'num_lines': 3}

# для массивов создать класс массивов, где будут храниться
# паспорта и значения 
class ArrPassport:
    def __init__(self, name):
        self.name = name

    def set_size(self, size):
        self.size = size
        self.arr = []
        for i in range(size):
            arr[i] = 0
            
    def get_element(self, num):
        if num < 0:
            print("negative index in", self.name)
            return ('Error')
        if num > self.size:
            print("out of array bounds", self.name)
            return ('Error')
        return arr[i]
    def set_element(self, pos, num):
        self.arr[pos] = num

variables = {}

def execute(operation, stack):
    if operation[0] == ':=':
        # if variables.has_key(op1[0]):
        #     if isinstance(variables[op2[0]], int):
        return (False)
    if operation[0] in :
        for elem in stack:
            variables[elem[0]] = 0
    if op2[1] == 'ID': #нужно все переписать
        if variables.has_key(op2[0]):
            if isinstance(variables[op2[0]], int):
                op2 = variables[op2[0]]
        else:
            return ('Error')
    if op2[1] == 'INT':
        op2 = op2[0]
    if op1[1] == 'INT':
        op1 = op1[0]
    if op1[1] == 'ID':
        if variables.has_key(op1[0]):
            if isinstance(variables[op1[0]], int):
                op1 = variables[op1[0]]
        else:
            pass
    if operation[0] == '+':
        return (True, (op1 + op2, 'INT'))
    if operation[0] == '-':
        return (True, (op1 - op2, 'INT'))
    if operation[0] == '*':
        return (True, (op1 * op2, 'INT'))
    if operation[0] == '/':
        return (True, (op1 / op2, 'INT'))
    
def take_tokens(tokens): #освновная функция, которой будут обращатся
    stack = []
    number = len(tokens)
    i = 0
    while i != number:
        if tokens[i][1] in ['ID','INT']:
            stack.append(tokens[i])
        elif tokens[i][1] == 'OPERATION':
            res = execute(tokens, stack)
            if res[0]:
                stack.insert(i+1, res)
                number +=1


if __name__ == '__main__': # зедсь можно тестить вызывая python3 rpn.py в консоли
    a = 2