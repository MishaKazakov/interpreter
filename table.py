
def next(term, not_term):
    if not_term[0] == 'P':
        if term[0] == 'num':
            return 'R', 'P'
        elif term[0] == 'arr':
            return ['R', 'P']
        elif term[0] == 'mtx':
            return ['R', 'P']
        elif term[0] == '{':
            return ['R','P','}']
        else:
            return ['Error', term]
    elif not_term[0] == 'R':
        if term[0] == 'a':
            return ['M']
        else:
            return ['Error', term]
    elif not_term[0] == 'M':
        if len(term) == 2 and term[0] == ',' and term[1] == 'a':
            return ['M']
        elif term[0] == ',' and len(term) == 1:
            return ['getNext', 'M']
        elif term[0] == ';':
            return ['deleteTerm']
        else:
            return ['Error', term]
    return ['Error', term]
