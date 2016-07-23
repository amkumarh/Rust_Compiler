#!/usr/bin/python
import lex
from collections import defaultdict

reserved = {
	'as' : 'AS',
    	'break' : 'BREAK',
    	'crate' : 'CRATE',
    	'else' : 'ELSE',
    	'enum' : 'ENUM',
    	'extern' : 'EXTERN',
    	'false' : 'FALSE',
    	'fn' : 'FN',
    	'for' : 'FOR',
    	'if' : 'IF',
    	'impl' : 'IMPL',
    	'in' : 'IN',
    	'let' : 'LET',
    	'loop' : 'LOOP',
	'main' : 'MAIN_FUN',
    	'match' : 'MATCH',
    	'mod' : 'MOD',
    	'move' : 'MOVE',
    	'mut' : 'MUT',
    	'pub' : 'PUB',
	#"println+!" : 'PRINTF_FUN',
    	'ref' : 'REF',
    	'return' : 'RETURN',
    	'static' : 'STATIC',
    	'selfValue' : 'SELFVALUE',
    	'selfType' : 'SELFTYPE',
    	'struct' : 'STRUCT',
    	'super' : 'SUPER',
    	'true' : 'TRUE',
    	'trait' : 'TRAIT',
    	'type' : 'TYPE',
    	'unsafe' : 'UNSAFE',
    	'use' : 'USE',
    	'virtual' : 'VIRTUAL',
    	'while' : 'WHILE',
    	'continue' : 'CONTINUE',
    	'box' : 'BOX',
    	'const' : 'CONST',
    	'where' : 'WHERE',
    	'proc' : 'PROC',
    	'alignof' : 'ALIGNOF',
    	'become' : 'BECOME',
    	'offsetof' : 'OFFSETOF',
    	'priv' : 'PRIV',
    	'pure' : 'PURE',
    	'sizeof' : 'SIZEOF',
    	'typeof' : 'TYPEOF',
    	'unsized' : 'UNSIZED',
    	'yield' : 'YIELD',
    	'do' : 'DO',
    	'abstract' : 'ABSTRACT',
    	'final' : 'FINAL',
    	'override' : 'OVERRIDE',
    	'macro' : 'MACRO',
	'i32' : 'i32'
}

tokens = [
	'PRINT',
	'SHEBANG_LINE',
	'SENTENCE',
	'ARROW',
	'ident',
	'LIT_INTEGER',
	'LESSEQUAL',
	'EQUALS_COMP',
	'ASSIGNMENT_OP',
	'BEGIN_BLOCK',
	'END_BLOCK',
	'OPEN_PARANTHESIS',
	'CLOSE_PARANTHESIS',
	'SEMICOLON',
	'COMMA',
	'DOT',
	'D_DOT',
	'MINUS',
	'NOTEQUAL',
	'PLUS',
     	'STRING',
	'MULTIPLICATION',
	'DIVISION',
	'D_COLON',	
	'COLON',
	'LIT_FLOAT',
	'AND_OP',
	'AND_LOGICAL',
	'OR_OP',
	'OR_LOGICAL',
	'XOR_OP',
	'NOT_OP',
	'LEFT_SHIFT',
	'RIGHT_SHIFT',
	'LESS_THAN',
	'GREATER_THAN',
	'GREATER_EQUAL_OP',
	'LESS_EQUAL_OP',
	'MODULUS',
	'OPEN_BRACKET',
	'CLOSE_BRACKET',
	'mat',
	
 ] + list(reserved.values())

t_ignore_WHITESPACE=r"\s"

def t_ignore_COMMENT(t):
	r"\//.*"

def t_PRINT(t):
	r"\println!"
	return t

def t_SHEBANG_LINE(t):
	r"\!\#"
	return t

def t_SENTENCE(t):
	r'\"(.+?)\"'
	return t


def t_mat(t):
	r"=>"
	return t

def t_ARROW(t):
	r'\->'
	return t

def t_ident(t):
    r"[&]?[a-zA-Z$_][\w$]*"
    t.type = reserved.get(t.value,'ident')    
    return t

def t_LIT_INTEGER(t):
    r"\d+"
    t.value = int(t.value)
    return t

def t_LESSEQUAL(t):				
	r"<=|"r"le"
	return t

def t_EQUALS_COMP(t):
	r"==|"r"eq"
	return t

def t_ASSIGNMENT_OP(t):
	r"="
	return t

def t_BEGIN_BLOCK(t):
	r"\{"
	return t

def t_END_BLOCK(t):
	r"\}"
	return t


def t_OPEN_PARANTHESIS(t):
	r"\("
	return t

def t_CLOSE_PARANTHESIS(t):
	r"\)"
	return t

def t_SEMICOLON(t):
	r";"
	return t

def t_COMMA(t):
	r","
	return t

def t_D_DOT(t):
	r"\.."
	return t

def t_DOT(t):
	r"\."
	return t

def t_MINUS(t):
	r"-"
	return t

def t_NOTEQUALS(t):
	r"\!=|"r"ne"
	return t

def t_PLUS(t):
	r"\+"
	return t

def t_STRING(t):
	r"\'([^\'])*\'"
	return t

def t_MULTIPLICATION(t):
	r"\*"
	return t

def t_DIVISION(t):
	r"/"
	return t

def t_D_COLON(t):
	r"\::"
	return t

def t_COLON(t):
	r"\:"
	return t

def t_LIT_FLOAT(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t

def t_AND_OP(t):
	r"&\&"
	return t

def t_AND_LOGICAL(t):
	r"\&"
	return t

def t_OR_OP(t):
	r"\|\|"
	return t

def t_OR_LOGICAL(t):
	r"\|"
	return t


def t_XOR_OP(t):
	r"\^"
	return t

def t_NOT_OP(t):
	r"\!|"r"not"
	return t

def t_LEFT_SHIFT(t):
	r"<<"
	return t

def t_RIGHT_SHIFT(t):
	r">>"
	return t

def t_GREATER_EQUAL_OP(t):
	r">=|"r"ge"
	return t

def t_LESS_EQUAL_OP(t):				
	r"<=|"r"le"
	return t

def t_LESS_THAN(t):
	r"<|"r"lt"
	return t

def t_GREATER_THAN(t):				
	r">|"r"gt"
	return t

def t_MODULUS(t):
	r"%"
	return t

def t_OPEN_BRACKET(t):
	r"\["
	return t

def t_CLOSE_BRACKET(t):
	r"\]"
	return t

#error	
def t_error(t):
	print "Illegal character %s" % t.value[0]
	t.lexer.skip(1)


lexer=lex.lex()
dic = {}
lis = defaultdict(list)
lis2 = []
lis3=[]
def runlexer(inputfile):
	program=open(inputfile).read()
	lexer.input(program)
	for tok in iter(lexer.token, None):
		if tok.type in dic:
			dic[tok.type] += 1
		else:
			dic[tok.type] = 1

		if tok.type in lis:
			if not tok.value in lis[tok.type]:
				lis[tok.type].append(tok.value)
		else:
			lis[tok.type].append(tok.value)
	for i in dic.keys():
		lis2.append(str(lis[i]))
				
	#print lis2
	for f in lis2:
		x=f.lstrip('[')
		x=x.rstrip(']')
		x=x.strip("'")
                lis3.append(x.rstrip("'"))
		
	#print lis3
        for jb in lis3:
		print jb
	


if __name__=="__main__":
	from sys import argv 
	filename, inputfile = argv
	runlexer(inputfile)
