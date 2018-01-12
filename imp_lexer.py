
import lexer

RESERVED  = 'RESERVED'
INT       = 'INT'
ID        = 'ID'
OPERATION = 'OPERATION'


token_exprs = [
    (r'[ \n\t]+',              None),
    (r'#[^\n]*',               None),
    (r'\:=',                   OPERATION),
    (r'\(',                    RESERVED),
    (r'\)',                    RESERVED),
    (r';',                     RESERVED),
    (r',',                     RESERVED),
    (r'\+',                    OPERATION),
    (r'-',                     OPERATION),
    (r'\*',                    OPERATION),
    (r'/',                     OPERATION),
    (r'<=',                    OPERATION),
    (r'<',                     OPERATION),
    (r'>=',                    OPERATION),
    (r'>',                     OPERATION),
    (r'!=',                    OPERATION),
    (r'=',                     OPERATION),
    (r'\[',                    RESERVED),
    (r'\]',                    RESERVED),
    (r'if',                    RESERVED),
    (r'then',                  RESERVED),
    (r'else',                  RESERVED),
    (r'while',                 RESERVED),
    (r'{',                     RESERVED),
    (r'}',                     RESERVED),
    (r'num',                   OPERATION),
    (r'arr',                   OPERATION),
    (r'mtx',                   OPERATION),
    (r'out',                   OPERATION),
    (r'in',                    OPERATION),
    (r'mem1',                  OPERATION),
    (r'mem2',                  OPERATION),
    (r'[0-9]+',                INT),
    (r'[A-Za-z][A-Za-z0-9_]*', ID),
]

def imp_lex(characters):
    return lexer.lex(characters, token_exprs)
