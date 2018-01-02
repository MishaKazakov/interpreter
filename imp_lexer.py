
import lexer

RESERVED = 'RESERVED'
INT      = 'INT'
ID       = 'ID'

token_exprs = [
    (r'[ \n\t]+',              None),
    (r'#[^\n]*',               None),
    (r'\:=',                   RESERVED),
    (r'\(',                    RESERVED),
    (r'\)',                    RESERVED),
    (r';',                     RESERVED),
    (r',',                     RESERVED),
    (r'\+',                    RESERVED),
    (r'-',                     RESERVED),
    (r'\*',                    RESERVED),
    (r'/',                     RESERVED),
    (r'<=',                    RESERVED),
    (r'<',                     RESERVED),
    (r'>=',                    RESERVED),
    (r'>',                     RESERVED),
    (r'!=',                    RESERVED),
    (r'=',                     RESERVED),
    (r'\[',                    RESERVED),
    (r'\]',                    RESERVED),
    (r'if',                    RESERVED),
    (r'then',                  RESERVED),
    (r'else',                  RESERVED),
    (r'while',                 RESERVED),
    (r'{',                     RESERVED),
    (r'}',                     RESERVED),
    (r'num',                   RESERVED),
    (r'arr',                   RESERVED),
    (r'mtx',                   RESERVED),
    (r'out',                   RESERVED),
    (r'in',                    RESERVED),
    (r'mem1',                  RESERVED),
    (r'mem2',                  RESERVED),
    (r'[0-9]+',                INT),
    (r'[A-Za-z][A-Za-z0-9_]*', ID),
]

def imp_lex(characters):
    return lexer.lex(characters, token_exprs)
