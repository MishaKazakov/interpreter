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

class Variable:
    def __init__(self):
        self.num = 0
    def set(self, num):
        self.num = num
    def get(self):
        return self.num
    

class ArrPassport:
    def __init__(self, name):
        self.name = name
        self.size = 0
        self.arr = []

    def set_size(self, size):
        self.size = size
        for i in range(size):
            self.arr.append(Variable())
            
    def get_element(self, num):
        if num < 0:
            print("negative index in", self.name)
            return ('Error')
        if num > self.size:
            print("out of array bounds", self.name)
            return ('Error')
        return self.arr[num]
    def set_element(self, pos, num):
        self.arr[pos].set(num)

def execute(operation, stack, variables):
    if operation[0] == 'num': #иницаилизация
        for elem in stack:
            if elem[0] in variables:
                return ('Error')
            variables[elem[0]] = Variable()     
        return
    op2 = stack.pop()
    op1 = stack.pop()
    if operation[0] == ':=':
        if isinstance(op1, Variable):
            if isinstance(op2, Variable):
                op1.set(op2.get())
                return
            elif op2[1] == 'INT':
                op1.set(int(op2[0]))
                return
            elif op2 == 'ID':
                if op2[0] in variables:
                    op1.set(variables[op2[0]].get())
                else:
                    return ('Error', 'used uninitialized variable ' + op2[0])
            else:
                return ('Error')
        if op1[1] == 'INT':
            return ('Error', 'assigment to constant')
        if op1[0] in variables:
            if isinstance(op2, Variable):
                variables[op1[0]].set(op2.get())
                return 
            elif op2[1] == 'INT':
                variables[op1[0]].set(int(op2[0]))
                return
            elif op2 == 'ID':
                if op2[0] in variables:
                    variables[op1[0]].set(variables[op2[0]].get())
                else:
                    return ('Error', 'used uninitialized variable ' + op2[0])
            else:
                return ('Error')
            #if isinstance(variables[op1[0]], ArrPassport):
        else:
            return ('Error', 'not initialized used' + op[1])
        return (False)

    if isinstance(op1, Variable):
        op1 = op1.get()
    if isinstance(op2, Variable):
        op2 = op1.get()
    if op1[1] == 'INT':
        op1 = int(op1[0])
    if op2[1] == 'INT':
        op2 = int(op1[0]) 
    if op1[1] == 'ID':
        if not op1[0] in variables:
            return ('Error', 'used uninitialized variable ' + op1[0])
        op1 = variables[op1[0]].get() 
    if op2[1] == 'ID':
        if not op2[0] in variables:
            return ('Error', 'used uninitialized variable ' + op2[0])
        op1 = variables[op1[0]].get() 

        
        
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
    variables = {}
    number = len(tokens)
    i = 0
    while i != number:
        if tokens[i][1] in ['ID','INT']:
            stack.append(tokens[i])
        elif tokens[i][1] == 'OPERATION':
            res = execute(tokens[i], stack, variables)
            # if res[0]:
            #     stack.insert(i+1, res)
            #     number +=1
        i +=1


if __name__ == '__main__': # зедсь можно тестить вызывая python3 rpn.py в консоли
    a = 2