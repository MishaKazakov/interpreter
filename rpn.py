import sys
class Variable:
    def __init__(self):
        self.num = 0
    def set(self, num):
        self.num = num
    def get(self):
        return self.num    

class ArrPassport:
    def __init__(self):
        self.size = 0
        self.arr = []

    def set_size(self, size):
        self.size = size
        for i in range(size):
            self.arr.append(Variable())

    def get_size(self):
        return self.size    

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

class MtxPassport:
    def __init__(self):
        self.mtx = []
        self.row = 0
        self.column = 0
    
    def set_size(self, row, column):
        self.row = row
        self.column = column
        for i in range(row):
            arr = ArrPassport()
            arr.set_size(self.column)
            self.mtx.append(arr)
    
    def get_element(self, row, column):
        return self.mtx[row].get_element(column)

def get_value(op, variables):
    if isinstance(op, Variable):
        op = op.get()
    elif op[1] == 'INT':
        op = int(op[0])
    elif op[1] == 'ID':
        if op[0] in variables:
            op = variables[op[0]].get()
        else:
            return ('Error', 'used uninitialized variable ' + op[0])
    return op

def execute(operation, stack, variables):
    # print(stack)
    # print(operation)
    if operation[0] == 'num': #иницаилизация
        for i in range(len(stack)):
            elem = stack.pop()
            if elem[0] in variables:
                return ('Error')
            variables[elem[0]] = Variable()     
        return
    
    if operation[0] == 'arr':
        for i in range(len(stack)):
            elem = stack.pop()
            if elem[0] in variables:
                return ('Error')
            variables[elem[0]] = ArrPassport()     
        return

    if operation[0] == 'mtx':
        for i in range(len(stack)):
            elem = stack.pop()
            if elem[0] in variables:
                return ('Error')
            variables[elem[0]] = MtxPassport()     
        return

    if operation[0] == 'mem1':
        lenght = stack.pop()
        lenght = get_value(lenght, variables)
        var = stack.pop()
        if var[0] in variables:
            if isinstance(variables[var[0]], ArrPassport):
                var = variables[var[0]]
                var.set_size(lenght)
                return
            else:
                return ('Error', 'using non array variable ' + var[0])
        else:
            return ('Error', 'used uninitialized variable ' + var[0])
    
    if operation[0] == 'mem2':
        column = stack.pop()
        column = int(column[0])
        row = stack.pop()
        row = int(row[0])
        var = stack.pop()
        if var[0] in variables:
            if isinstance(variables[var[0]], MtxPassport):
                var = variables[var[0]]
                var.set_size(row, column)
                return
            else:
                return ('Error', 'using non array variable ' + var[0])
        else:
            return ('Error', 'used uninitialized variable ' + var[0])
    
    if operation[0] == 'I':
        pos = stack.pop()
        pos = get_value(pos, variables)
        var = stack.pop()
        if var[0] in variables:
            if isinstance(variables[var[0]], ArrPassport):
                var = variables[var[0]]
                stack.append(var.get_element(pos))
                return
            else:
                return ('Error', 'using non array variable ' + var[0])
        else:
            return ('Error', 'used uninitialized variable ' + var[0])

    if operation[0] == 'I2':
        column = stack.pop()
        column = int(column[0])
        row = stack.pop()
        row = int(row[0])
        var = stack.pop()
        if var[0] in variables:
            if isinstance(variables[var[0]], MtxPassport):
                var = variables[var[0]]
                stack.append(var.get_element(row,column))
                return
            else:
                return ('Error', 'using non array variable ' + var[0])
        else:
            return ('Error', 'used uninitialized variable ' + var[0])

    if operation[0] == 'jf':
        tag = stack.pop()
        res = stack.pop()
        if res[0] == 'false':
            return ('jump', tag[1])
        return
    
    if operation[0] == 'j':
        tag = stack.pop()
        return ('jump', tag[1])
    
    if operation[0] == 'in':
        try:
            mode=int(input())
        except ValueError:
            return ('Error', 'not a number in input')
        op = stack.pop()
        if isinstance(op, Variable):
            op.set(mode)
            return
        elif op[1] == 'ID':
            if op[0] in variables:
                variables[op[0]].set(mode)
                return
            else:
                return ('Error', 'used uninitialized variable ' + op[0])
        else:
            return ('Error', 'wrong input')
    if operation[0] == 'out':
        op = stack.pop()
        if isinstance(op, Variable):
            print(op.get())
            return
        elif op[1] == 'ID':
            if op[0] in variables:
                print(variables[op[0]].get())
                return
            else:
                return ('Error', 'used uninitialized variable ' + op[0])
        else:
            print(op[0])
            return

    if operation[0] == 'unary_minus':
        op = stack.pop()
        if isinstance(op, Variable):
            op.set(-op.get())
        elif op[1] == 'INT':
            op = (-op[0], 'INT')
        elif op[1] == 'ID':
            if op[0] in variables:
                variables[op[0]].set(-variables[op[0]].get())
        stack.append(op)
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
            elif op2[1] == 'ID':           
                if op2[0] in variables:
                    op1.set(variables[op2[0]].get())
                    return
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
            elif op2[1] == 'ID':
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
    elif op1[1] == 'INT':
        op1 = int(op1[0])
    elif op1[1] == 'ID':
        if not op1[0] in variables:
            return ('Error', 'used uninitialized variable ' + op1[0])
        op1 = variables[op1[0]].get() 

    if isinstance(op2, Variable):
        op2 = op2.get()
    elif op2[1] == 'INT':
        op2 = int(op2[0]) 
    elif op2[1] == 'ID':
        if not op2[0] in variables:
            return ('Error', 'used uninitialized variable ' + op2[0])
        op2 = variables[op2[0]].get() 
    
    if operation[0] == '+':
        stack.append((op1 + op2, 'INT'))
        return (True, (op1 + op2, 'INT'))
    if operation[0] == '-':
        stack.append((op1 - op2, 'INT'))
        return (True, (op1 - op2, 'INT'))
    if operation[0] == '*':
        stack.append((op1 * op2, 'INT'))
        return (True, (op1 * op2, 'INT'))
    if operation[0] == '/':
        stack.append((op1 / op2, 'INT'))
        return (True, (op1 / op2, 'INT'))

    if operation[0] == '<':
        if op1 < op2:
            stack.append(('true', 'RESERVED'))
            return
        else:
            stack.append(('false', 'RESERVED'))
            return
    if operation[0] == '>':
        if op1 > op2:
            stack.append(('true', 'RESERVED'))
            return
        else:
            stack.append(('false', 'RESERVED'))
            return
    if operation[0] == '=':
        if op1 == op2:
            stack.append(('true', 'RESERVED'))
            return
        else:
            stack.append(('false', 'RESERVED'))
            return
    if operation[0] == '!=':
        if op1 != op2:
            stack.append(('true', 'RESERVED'))
            return
        else:
            stack.append(('false', 'RESERVED'))
            return
    
def take_tokens(tokens): #освновная функция, которой будут обращатся
    stack = []
    variables = {}
    number = len(tokens)
    i = 0
    while i != number:
        if tokens[i][1] == 'OPERATION':
            res = execute(tokens[i], stack, variables)
            if res:
                if res[0] == 'jump':
                    i = res[1] -1
                elif res[0] == 'Error':
                    print(res[1])
                    break
        else:
            stack.append(tokens[i])
        i +=1
    # for key, value in variables.items():
    #     print(key, value.get())
    #     for i in range(value.get_size()):
    #         print(value.get_element(i).get())

if __name__ == '__main__': # зедсь можно тестить вызывая python3 rpn.py в консоли
    a = 2