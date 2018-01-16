import string
import sys
def lex(characters):
    pos = 0
    tokens = []
    state = 's'
    elem = None
    reserved_words = ['if', 'else', 'while']
    operations = ['num', 'arr', 'mtx', 'out', 'in', 'mem1', 'mem2']
    while pos < len(characters):
        if state == 's':
            if characters[pos].isdigit():
                elem = characters[pos]
                state = 'i'
            elif characters[pos] in string.ascii_letters:
                elem = characters[pos]
                state = 'p'
            elif characters[pos] in ':<>!':
                elem = characters[pos]
                state = 'n'
            elif characters[pos] in r'+-*/=':
                elem = characters[pos]
                tokens.append(operation(elem))
                state = 's'
            elif characters[pos] in ' \n\t':
                state = 's'
            elif characters[pos] in r'();,[]{}':
                elem = characters[pos]
                tokens.append(reserved(elem))
                state = 's'
            else:
                exit(pos,  characters)  
        elif state == 'i':
            if characters[pos].isdigit():
                elem += characters[pos]
            else:
                tokens.append(is_int(elem))
                if characters[pos] in string.ascii_letters:
                    elem = characters[pos]
                    state = 'p'
                elif characters[pos] in ':<>!':
                    elem = characters[pos]
                    state = 'n'
                elif characters[pos] in r'+-*/=':
                    elem = characters[pos]
                    tokens.append(operation(elem))
                    state = 's'
                elif characters[pos] in r' \n\t':
                    state = 's'
                elif characters[pos] in r'();,[]{}':
                    elem = characters[pos]
                    tokens.append(reserved(elem))
                    state = 's'                        
        elif state == 'p':
            if characters[pos] in string.ascii_letters:
                elem += characters[pos]
            elif characters[pos].isdigit():
                elem += str(characters[pos])
            elif characters[pos] in ' \n\t':
                state = 's'
                if elem in reserved_words:
                    tokens.append(reserved(elem))
                elif elem in operations:
                    tokens.append(operation(elem))
                else:
                    tokens.append(is_id(elem))
            elif characters[pos] in ',':
                state = 's'
                tokens.append(is_id(elem))
                elem = characters[pos]
                tokens.append(reserved(elem))
            elif characters[pos] in r'();[]{}':
                if elem in reserved_words:
                    tokens.append(reserved(elem))
                elif elem in operations:
                    tokens.append(operation(elem))
                else:
                    tokens.append(is_id(elem))
                elem = characters[pos]
                tokens.append(reserved(elem))
                state = 's'
            elif characters[pos] in ':<>!':
                if elem in reserved_words:
                    tokens.append(reserved(elem))
                elif elem in operations:
                    tokens.append(operation(elem))
                else:
                    tokens.append(is_id(elem))
                elem = characters[pos]
                state = 'n'
            elif characters[pos] in r'+-*/=':
                if elem in reserved_words:
                    tokens.append(reserved(elem))
                elif elem in operations:
                    tokens.append(operation(elem))
                else:
                    tokens.append(is_id(elem))
                elem = characters[pos]
                tokens.append(operation(elem))
                state = 's'
            else:
                exit(pos,  characters)
        elif state == 'n':
            if characters[pos] == '=':
                elem += characters[pos]
                tokens.append(operation(elem))
                state = 's'
            elif characters[pos].isdigit():
                tokens.append(operation(elem))
                elem = characters[pos]
                state = 'i'
            elif characters[pos] in string.ascii_letters:
                tokens.append(operation(elem))
                elem = characters[pos]
                state = 'p'  
            elif characters[pos] in r' \n\t':
                tokens.append(operation(elem))
                state = 's'
            elif characters[pos] in r'();,[]{}':
                tokens.append(operation(elem))
                elem = characters[pos]
                tokens.append(reserved(elem))
                state = 's'
        pos += 1
    return tokens

def is_id(elem):
    return (elem, 'ID')
def is_int(elem):
    return (elem, 'INT')
def operation(elem):
    return (elem, 'OPERATION')
def reserved(elem):
    return (elem, 'RESERVED')

def exit(pos, characters):
    #sys.stderr.write('Illegal character: %s\n' % characters[pos])
    sys.stderr.write('Illegal character:' + characters[pos] + str(pos) + '\n')
    sys.exit(1)  


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename) as characters:
        for line in characters:
            tokens = lex(line)
            print(tokens)