
import sys
from imp_lexer import *
# from rpn import *    
global else_flag
global if_flag
global if_end_flag
def get_priority(priorities_list,op):
    for i in range(len(priorities_list)):
        if priorities_list[i].count(op):
            return i

def priorities(op1, op2):
    priorities_list = [
        ['*','/'],
        ['+', '-'],
        ['('],[')'],
        [':=', 'mem1', 'mem2'],
        ['<', '>', '=', '!=', 'jf', 'j', 'tag1', 'tag2', 'while_tag1', 'while_tag2']
    ]
    priority1 = get_priority(priorities_list, op1)
    priority2 = get_priority(priorities_list, op2)

    if priority2 >= priority1:
        return True
    else:
        return False

def generator_new_item(generator,operation_generator, term):
    if term[0] == ')':
        prev_term = operation_generator.pop()
        while prev_term[0] != '(':
            generator.append(prev_term)
            prev_term = operation_generator.pop()
    elif term[0] == '(':
        operation_generator.append(term)
    else:
        while len(operation_generator) != 0 and priorities(operation_generator[len(operation_generator) - 1][0], term[0]):
            generator.append(operation_generator.pop())
        if term[0] == 'j':
            generator.append(term)
        else:
            operation_generator.append(term)

def generator_end(generator,operation_generator):
    global else_flag
    global if_end_flag
    for i in range(len(operation_generator)):
        generator.append(operation_generator.pop())
    if else_flag:
        after_else(generator)
        else_flag = False
    if if_end_flag:
        end_of_if(generator)
        if_end_flag = False
    operation_generator.clear()

def if_required(generator, operation_generator):
    generator_new_item(generator,operation_generator, ('tag2', 'go_next'))
    generator_new_item(generator,operation_generator, ('j', 'RESERVED'))
    
def end_of_if(generator):
    position = generator.index(('tag1', 'RESERVED'))
    generator[position] = ('tag1', len(generator))

def else_postion(generator,operation_generator):
    if_required(generator, operation_generator)
    position = generator.index(('tag1', 'RESERVED'))
    generator[position] = ('tag1', len(generator))

def after_else(generator):
    position = generator.index(('tag2', 'go_next'))
    generator[position] = ('tag2', len(generator)) #might be a problem with mytipal

def next_items(term, not_term,generator, operation_generator):
    global if_flag
    global else_flag
    global if_end_flag
    if not_term[0] == 'P':
        else_flag = False
        if_end_flag = False
        if term[0][0] == 'num':
            operation_generator.append(term[0])
            return 'R', 'P'
        elif term[0][0] == 'arr':
            operation_generator.append(term[0])
            return ['R', 'P']
        elif term[0][0] == 'mtx':
            operation_generator.append(term[0])
            return ['R', 'P']
        elif term[0][0] == '{':
            return ['A','Q','endOfMain']
        else:
            return ['Error', term]
    elif not_term[0] == 'endOfBody':
        if term[0][0] == '}':
            return ['deleteTerm']
        else:
            return ['Error', 'not closed bracket']
    elif not_term[0] == 'endOfMain':
        if term[0][0] == '}':
            generator_end(generator, operation_generator)
            return ['end']
        else:
            return ['Error', 'not closed bracket in the main']
    elif not_term[0] == 'R':
        if term[0][1] == 'ID':
            generator.append(term[0])
            return ['M']
        else:
            return ['Error', term]
    elif not_term[0] == 'M': # may be problem with many operands
        if len(term) == 2 and term[0][0] == ',' and term[1][1] == 'ID':
            generator.append(term[1])
            return ['M']
        elif len(term) == 1 and term[0][0] == ',':
            return ['getNext', 'M']
        elif term[0][0] == ';':
            generator_end(generator, operation_generator)
            #rpn execute
            return ['deleteTerm']
        else:
            return ['Error', term]
    elif not_term[0] == 'A':
        if term[0][0] == '{':
            if if_flag:
                for i in range(len(operation_generator)):
                    generator.append(operation_generator.pop())
                if_flag = False
            return ['A','Q', 'endOfBody']
        elif term[0][0] == 'if':
            operation_generator.append(('jf', 'RESERVED'))
            operation_generator.append(('tag1', 'RESERVED'))
            return ['C', 'A', 'E', 'Z']
        elif term[0][0] == 'while':
            return ['C', 'A', 'Z']
        elif term[0][0] == 'in' and len(term) == 1:
            return ['getNext', 'A']
        elif len(term) == 2 and term[0][0] == 'in' and term[1][1] == 'ID':
            generator.append(term[1])
            operation_generator.append(term[0])
            return ['H']
        elif term[0][0] == 'out':
            operation_generator.append(term[0])
            return ['S']
        elif len(term) == 1 and term[0][0] == 'mem1':
            return ['getNext', 'A']
        elif len(term) == 2 and term[0][0] == 'mem1' and term[1][1] == 'ID':
            operation_generator.append(term[0])
            generator.append(term[1])
            return ['S']
        elif len(term) == 1 and term[0][0] == 'mem2':
            return ['getNext', 'A']
        elif len(term) == 2 and term[0][0] == 'mem2' and term[1][1] == 'ID':
            operation_generator.append(term[0])
            generator.append(term[1])
            return ['S', 'S']
        elif term[0][1] == 'ID':
            generator.append(term[0])
            return ['H', 'assignment']
        else:
            return ['Error', term]
    elif not_term[0] == 'assignment':
        if term[0][0] == ':=':
            generator_new_item(generator,operation_generator, term[0])
            return ['S', 'Z']
        else:
            return ['Error', 'assignment']
    elif not_term[0] == 'Q':
        if term[0][0] == ';':
            generator_end(generator, operation_generator)
            return ['A', 'Q']
        else:
            return ['tryNextTerm']
    elif not_term[0] == 'E':
        if term[0][0] == 'else':
            else_flag = True
            else_postion(generator, operation_generator)
            return ['A']
        else:
            if_end_flag = True
            return ['tryNextTerm']
    elif not_term[0] == 'C':
        if term[0][0] == '(':
            generator_new_item(generator,operation_generator, term[0])
            return ['S', ')', 'V', 'U', 'D']
        elif term[0][1] == 'ID':
            generator.append(term[0])
            return ['H', 'V', 'U', 'D']
        elif term[0][1] == 'INT':
            generator.append(term[0])
            return ['V', 'U', 'D']
        elif term[0][1] == '+':
            return ['G','V', 'U']
        elif term[0][1] == '-':
            operation_generator.append(('unary_minus', 'RESERVED'))
            return ['G','V', 'U']
        else:
            return ['Error', term]
    elif not_term[0] == ')':
        if term[0][0] == ')':
            generator_new_item(generator,operation_generator, term[0])
            return ['deleteTerm']
        else:
            return ['Error', term]
    elif not_term[0] == 'D':
        if_flag = True
        if term[0][0] == '<':
            operation_generator.append(term[0])
            return ['S', 'Z']
        elif term[0][0] == '>':
            operation_generator.append(term[0])
            return ['S', 'Z']
        elif term[0][0] == '=':
            operation_generator.append(term[0])
            return ['S', 'Z']
        elif term[0][0] == '!=':
            operation_generator.append(term[0])
            return ['S', 'Z']
        else:
            return ['Error', term]
    elif not_term[0] == 'S':
        if term[0][0] == '(':
            generator_new_item(generator,operation_generator, term[0])
            return ['S', ')', 'V', 'U']
        elif term[0][1] == 'ID':
            generator.append(term[0])
            return ['H', 'V', 'U']
        elif term[0][1] == 'INT':
            generator.append(term[0])
            return ['V', 'U']
        elif term[0][0] == '+': #todo
            return ['G', 'V', 'U']
        elif term[0][0] == '-':
            operation_generator.append(('unary_minus', 'RESERVED'))
            return ['G', 'V', 'U']
        else:
            return ['Error', term]
    elif not_term[0] == 'U':
        if term[0][0] == '+':
            generator_new_item(generator,operation_generator, term[0])
            return ['T', 'U']
        elif term[0][0] == '-':
            generator_new_item(generator,operation_generator, term[0])
            return ['T', 'U']
        else:
            return ['tryNextTerm']
    elif not_term[0] == 'T':
        if term[0][0] == '(':
            generator_new_item(generator,operation_generator, term[0])
            return ['S', ')', 'V']
        elif term[0][1] == 'ID':
            generator.append(term[0])
            return ['H', 'V']
        elif term[0][1] == 'INT':
            generator.append(term[0])
            return ['V']
        elif term[0][0] == '+':
            return ['G', 'V']
        elif term[0][0] == '-':
            operation_generator.append(('unary_minus', 'RESERVED'))
            return ['G', 'V']
        else:
            return ['Error', term]
    elif not_term[0] == 'V':
        if term[0][0] == '*':
            generator_new_item(generator,operation_generator, term[0])
            return ['F', 'V']
        elif term[0][0] == '/':
            generator_new_item(generator,operation_generator, term[0])
            return ['F', 'V']
        else:
            return ['tryNextTerm']
    elif not_term[0] == 'F':
        if term[0][0] == '(':
            generator_new_item(generator,operation_generator, term[0])
            return ['S', ')']
        elif term[0][1] == 'ID':
            generator.append(term[0])
            return ['H']
        elif term[0][1] == 'INT':
            generator.append(term[0])
            return ['deleteTerm'] #todo
        elif term[0][0] == '+':
            return ['G', 'V']
        elif term[0][0] == '-':
            operation_generator.append(('unary_minus', 'RESERVED'))
            return ['G', 'V']
        else:
            return ['Error', term]
    elif not_term[0] == 'G':
        if term[0][0] == '(':
            generator_new_item(generator,operation_generator, term[0])
            return ['S', ')']
        elif term[0][1] == 'ID':
            generator.append(term[0])
            return ['H']
        elif term[0][1] == 'INT':
            generator.append(term[0])
            return ['deleteTerm'] #todo
        else:
            return ['Error', term]
    elif not_term[0] == 'H':
        if term[0][0] == '[':
            return ['S', 'K']
        else:
            return ['tryNextTerm']
    elif not_term[0] == 'K':
        if term[0][0] == ']':
            return ['deleteTerm']
        elif term[0][0] == ',':
            return ['S', 'square_bracket']
        else:
            return ['Error', term]
    elif not_term[0] == 'square_bracket':
        if term[0][0] == ']':
            return ['deleteTerm']
        else:
            return ['Error', term]
    elif not_term[0] == 'Z':            
        return ['tryNextTerm']
    return ['Error', term]



if __name__ == '__main__':
    generator = []
    operation_generator = [] 
    filename = sys.argv[1]
    with open(filename) as characters:
        not_term = ['P']
        flag = False
        terms = []
        Error = False
        line_num = 0
        for line in characters:
            tokens = imp_lex(line)            
            line_num += 1
            for token in tokens:  
                try_next_term_flag = True      
                if flag:
                    flag = False
                else:
                    terms = []
                terms.append(token)

                while True:
                    new_not_terms = next_items(terms, not_term, generator, operation_generator)
                    del not_term[0]
                    for number in range(len(new_not_terms)):
                        not_term.insert(number, new_not_terms[number])
                    if not_term[0] == 'deleteTerm':
                        del not_term[0]   
                    if not_term[0] == 'tryNextTerm':
                        del not_term[0] 
                        continue
                    if not_term[0] != 'tryNextTerm':
                        break 
                                  
                if not_term[0] == 'getNext':
                    del not_term[0]
                    flag = True
                    continue
                if not_term[0] == 'Error':
                    print('Error in line',line_num, ' with ' ,not_term[1])
                    Error = True
                    break
                a = [[('a', 'ID')], ('b', 'ID'), [('num', 'RESERVED')]]
    print(generator)