
import sys
from imp_lexer import *
from rpn import *    


def next_items(term, not_term,generator):
    if not_term[0] == 'P':
        if term[0][0] == 'num':
            generator.append([term])
            return 'R', 'P'
        elif term[0][0] == 'arr':
            generator.append([term])
            return ['R', 'P']
        elif term[0][0] == 'mtx':
            generator.append([term])
            return ['R', 'P']
        elif term[0][0] == '{':
            return ['A','Q','endOfMain']
        else:
            return ['Error', term]
    elif not_term[0] == 'endOfBody':
        if term[0][0] == '}':
            return ['deleteTerm']
        else:
            return ['Error', 'not closed bracket in the body']
    elif not_term[0] == 'endOfMain':
        if term[0][0] == '}':
            return ['end']
        else:
            return ['Error', 'not closed bracket in the body']
    elif not_term[0] == 'R':
        if term[0][1] == 'ID':
            generator[len(generator) - 1].insert(0, term)
            return ['M']
        else:
            return ['Error', term]
    elif not_term[0] == 'M':
        if len(term) == 2 and term[0][0] == ',' and term[1][1] == 'ID':
            generator[len(generator) - 1].insert(0, term[1])
            return ['M']
        elif len(term) == 1 and term[0][0] == ',':
            return ['getNext', 'M']
        elif term[0][0] == ';':
            return ['deleteTerm']
        else:
            return ['Error', term]
    elif not_term[0] == 'A':
        if term[0][0] == '{':
            return ['A','Q', 'endOfBody']
        elif term[0][0] == 'if':
            return ['C', 'A', 'E', 'Z']
        elif term[0][0] == 'while':
            return ['C', 'A', 'Z']
        elif term[0][0] == 'in' and len(term) == 1:
            return ['getNext', 'A']
        elif len(term) == 2 and term[0][0] == 'in' and term[1][1] == 'ID':
            return ['H']
        elif term[0][0] == 'out':
            return ['S']
        elif len(term) == 1 and term[0][0] == 'mem1':
            return ['getNext', 'A']
        elif len(term) == 2 and term[0][0] == 'mem1' and term[1][1] == 'ID':
            return ['S']
        elif len(term) == 1 and term[0][0] == 'mem2':
            return ['getNext', 'A']
        elif len(term) == 2 and term[0][0] == 'mem2' and term[1][1] == 'ID':
            return ['S', 'S']
        elif term[0][1] == 'ID':
            return ['H', 'assignment']
        else:
            return ['Error', term]
    elif not_term[0] == 'assignment':
        if term[0][0] == ':=':
            return ['S', 'Z']
        else:
            return ['Error', 'assignment']
    elif not_term[0] == 'Q':
        if term[0][0] == ';':
            return ['A', 'Q']
        else:
            return ['tryNextTerm']
    elif not_term[0] == 'E':
        if term[0][0] == 'else':
            return ['A']
        else:
            return ['tryNextTerm']
    elif not_term[0] == 'C':
        if term[0][0] == '(':
            return ['S', ')', 'V', 'U', 'D']
        elif term[0][1] == 'ID':
            return ['H', 'V', 'U', 'D']
        elif term[0][1] == 'INT':
            return ['V', 'U', 'D']
        elif term[0][1] == '+':
            return ['G','V', 'U']
        elif term[0][1] == '-':
            return ['G','V', 'U']
        else:
            return ['Error', term]
    elif not_term[0] == 'D':
        if term[0][0] == '<':
            return ['S', 'Z']
        elif term[0][0] == '>':
            return ['S', 'Z']
        elif term[0][0] == '=':
            return ['S', 'Z']
        elif term[0][0] == '!=':
            return ['S', 'Z']
        else:
            return ['Error', term]
    elif not_term[0] == 'S':
        if term[0][0] == '(':
            return ['S', ')', 'V', 'U']
        elif term[0][1] == 'ID':
            return ['H', 'V', 'U']
        elif term[0][1] == 'INT':
            return ['V', 'U']
        elif term[0][0] == '+':
            return ['G', 'V', 'U']
        elif term[0][0] == '-':
            return ['G', 'V', 'U']
        else:
            return ['Error', term]
    elif not_term[0] == 'U':
        if term[0][0] == '+':
            return ['T', 'U']
        elif term[0][0] == '-':
            return ['T', 'U']
        else:
            return ['tryNextTerm']
    elif not_term[0] == 'T':
        if term[0][0] == '(':
            return ['S', ')', 'V']
        elif term[0][1] == 'ID':
            return ['H', 'V']
        elif term[0][1] == 'INT':
            return ['V']
        elif term[0][0] == '+':
            return ['G', 'V']
        elif term[0][0] == '-':
            return ['G', 'V']
        else:
            return ['Error', term]
    elif not_term[0] == 'V':
        if term[0][0] == '*':
            return ['F', 'V']
        elif term[0][0] == '/':
            return ['F', 'V']
        else:
            return ['tryNextTerm']
    elif not_term[0] == 'F':
        if term[0][0] == '(':
            return ['S', ')']
        elif term[0][1] == 'ID':
            return ['H']
        elif term[0][1] == 'INT':
            return ['deleteTerm'] #todo
        elif term[0][0] == '+':
            return ['G', 'V']
        elif term[0][0] == '-':
            return ['G', 'V']
        else:
            return ['Error', term]
    elif not_term[0] == 'G':
        if term[0][0] == '(':
            return ['S', ')']
        elif term[0][1] == 'ID':
            return ['H']
        elif term[0][1] == 'INT':
            return ['deleteTerm'] #todo
        elif term[0][0] == '+':
            return ['G']
        elif term[0][0] == '-':
            return ['G', 'Z']
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
            return ['S', ']']
        else:
            return ['Error', term]
    elif not_term[0] == 'Z':
        return ['tryNextTerm']
    return ['Error', term]



if __name__ == '__main__':
    generator = []
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
                print(terms)
                while True:
                    new_not_terms = next_items(terms, not_term, generator)
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
                print(not_term)
                
    #print(generator)