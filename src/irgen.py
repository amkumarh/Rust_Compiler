import yacc
import sys
import subprocess
import re

from symbol_table1 import *
from copy import deepcopy

counter = 0
globaltemp=0
import lex
from lexer import *

lis = []
lis2 =[]
threeAC = []

line = 0
SCOPE = Env()
success = True

class tree:
	def __init__(self,name):
		self.name = name
		self.place = ""

def newtemp():
	global globaltemp
	globaltemp+= 1
	return "t"+ str(globaltemp)

def lineno():
	global line
	line += 1
	return line


def p_compilation_unit(p):
	''' compilation_unit : ProgramFile '''
	p[0]=p[1]

def p_ProgramFile(p):
	''' ProgramFile : fun_def main_fun
		| main_fun '''	
	

def p_main_fun(p):
	''' main_fun : FN MAIN_FUN OPEN_PARANTHESIS CLOSE_PARANTHESIS BEGIN_BLOCK stmts END_BLOCK '''

	
def p_fun_def(p):
	''' fun_def : FN ident OPEN_PARANTHESIS arguments CLOSE_PARANTHESIS BEGIN_BLOCK stmts END_BLOCK
		| FN ident OPEN_PARANTHESIS CLOSE_PARANTHESIS BEGIN_BLOCK stmts END_BLOCK
		| fun_def  FN ident OPEN_PARANTHESIS arguments CLOSE_PARANTHESIS BEGIN_BLOCK stmts END_BLOCK
		| fun_def FN ident OPEN_PARANTHESIS CLOSE_PARANTHESIS BEGIN_BLOCK stmts END_BLOCK'''
	

def p_stmts(p):
	''' stmts : non_block_stmt
		| non_block_stmt stmts
		| block_stmt 
		| block_stmt stmts 
		'''
	lis.append(p.slice)

def p_non_block_stmt(p):
	''' non_block_stmt : LET ident ASSIGNMENT_OP SENTENCE SEMICOLON
		| LET ident ASSIGNMENT_OP LIT_INTEGER SEMICOLON
		| LET ident ASSIGNMENT_OP LIT_FLOAT SEMICOLON
		| LET ident ASSIGNMENT_OP MINUS LIT_INTEGER SEMICOLON
		| LET ident ASSIGNMENT_OP TRUE SEMICOLON
		| LET ident ASSIGNMENT_OP FALSE SEMICOLON
		| LET MUT ident ASSIGNMENT_OP LIT_INTEGER SEMICOLON
		| LET MUT ident ASSIGNMENT_OP LIT_FLOAT SEMICOLON
		| LET MUT ident ASSIGNMENT_OP TRUE SEMICOLON
		| LET MUT ident ASSIGNMENT_OP FALSE SEMICOLON
		| PRINT OPEN_PARANTHESIS SENTENCE CLOSE_PARANTHESIS SEMICOLON 
		| binop
		| bitop
		| fn_call
		| print_ident '''
	lis.append(p.slice)
	#if (p[1] != "let" or len(p[2]) == 0) :
	 #       print "[Number Declaration] Error at line ",p.lineno(1)," : Variable not declared properly"
	  #      p_error(p)
	
    	#else:
	if (len(p) == 6 ) :
		temp = newtemp();
		tempdict = {}
		tempdict['place'] = temp
		SCOPE.add_entry(p[2],tempdict)
		threeAC.append(str(lineno()) + ", " + "=, " + temp + ", " + str(p[4]))

	elif (len(p) == 7 and p[4] =='-') :
		temp = newtemp();
		tempdict = {}
		tempdict['place'] = temp
		SCOPE.add_entry(p[2],tempdict)
		threeAC.append(str(lineno()) + ", " + "=, " + temp + ", " + str(p[4]) + str(p[5]))

	elif (len(p) == 7) :
		temp = newtemp();
		tempdict = {}
		tempdict['place'] = temp
		SCOPE.add_entry(p[3],tempdict)
		threeAC.append(str(lineno()) + ", " + "=, " + temp + ", " + str(p[5]))

def p_print_ident(p):
	''' print_ident : PRINT ident SEMICOLON '''
	temp = SCOPE.get_attribute_value(p[2],'place')
	threeAC.append(str(lineno()) + ", print, " + temp)


def p_binop(p):
	''' binop : ident ASSIGNMENT_OP expr SEMICOLON '''
	lis.append(p.slice)
	temp1 = SCOPE.get_attribute_value(p[1],'place')
	threeAC.append(str(lineno()) + ", " + "=, " + temp1 + ", " + p[3].place)
	
	
def p_expr(p):
	''' expr : ident
		| expr arith_op ident '''
	lis.append(p.slice)
	if len(p) == 2:
		temp = SCOPE.get_attribute_value(p[1],'place')		
		p[0]=tree("expr")
		p[0].place = temp
	
	else:
		temp = newtemp()
		temp1 = SCOPE.get_attribute_value(p[3],'place')
		temp2 = p[1].place
		threeAC.append(str(lineno()) + ", " + p[2].place + ", " + temp + ", " + temp2 + ", " + temp1)	
		p[0]=tree("expr")
		p[0].place = temp
		

def p_arith_op(p):
	''' arith_op : PLUS
		| MINUS
		| MULTIPLICATION
		| DIVISION
		| MODULUS '''
	lis.append(p.slice)
	p[0] = tree("arith_op")
	p[0].place = p[1]

def p_bitop(p):
	''' bitop : ident ASSIGNMENT_OP b_expr SEMICOLON '''
	lis.append(p.slice)
	temp1 = SCOPE.get_attribute_value(p[1],'place')
	threeAC.append(str(lineno()) + ", " + "=, " + temp1 + ", " + p[3].place)
	

def p_b_expr(p):
	''' b_expr : ident
		| b_expr bit_op ident '''
	lis.append(p.slice)
	if len(p) == 2:
		temp = SCOPE.get_attribute_value(p[1],'place')		
		p[0]=tree("b_expr")
		p[0].place = temp
	
	else:
		temp = newtemp()
		temp1 = SCOPE.get_attribute_value(p[3],'place')
		temp2 = p[1].place
		threeAC.append(str(lineno()) + ", " + p[2].place + ", " + temp + ", " + temp1 + ", " + temp2)	
		p[0]=tree("expr")
		p[0].place = temp

def p_bit_op(p):
	''' bit_op : AND_LOGICAL
		| OR_LOGICAL
		| XOR_OP
		| NOT_OP
		| LEFT_SHIFT
		| RIGHT_SHIFT '''
	lis.append(p.slice)
	p[0] = tree("bit_op")
	p[0].place = p[1]
 
def p_fn_call(p) :
	''' fn_call : ident OPEN_PARANTHESIS arguments CLOSE_PARANTHESIS SEMICOLON 
		| ident OPEN_PARANTHESIS CLOSE_PARANTHESIS SEMICOLON'''
	


def p_arguments(p):
	''' arguments : ident
		| ident COMMA arguments '''
		
	lis.append(p.slice)


def p_block_stmt(p):
	''' block_stmt : loop_block
		| while_block
		| for_block 
		| if_block 
		| if_else_block
		| else_if_block
		| unsafe_block 
		| match_block
		| struct_block '''
	lis.append(p.slice)

def p_loop_block(p):
	''' loop_block : LOOP BEGIN_BLOCK stmts END_BLOCK'''	
	lis.append(p.slice)

def p_while_block(p):
	''' while_block : WHILE TRUE BEGIN_BLOCK stmts END_BLOCK 
		| WHILE FALSE BEGIN_BLOCK stmts END_BLOCK 
		| WHILE ident BEGIN_BLOCK stmts END_BLOCK
		| WHILE ident EQUALS_COMP LIT_INTEGER BEGIN_BLOCK stmts END_BLOCK 
		| WHILE ident EQUALS_COMP LIT_FLOAT BEGIN_BLOCK stmts END_BLOCK '''
	lis.append(p.slice)

def p_for_block(p):
	''' for_block : FOR ident IN LIT_INTEGER D_DOT LIT_INTEGER BEGIN_BLOCK stmts END_BLOCK '''
	lis.append(p.slice)

def p_if_block(p):
	''' if_block : IF OPEN_PARANTHESIS ident operator LIT_INTEGER CLOSE_PARANTHESIS BEGIN_BLOCK stmts END_BLOCK
		| IF OPEN_PARANTHESIS ident operator EQUALS_COMP LIT_FLOAT CLOSE_PARANTHESIS BEGIN_BLOCK stmts END_BLOCK '''
	lis.append(p.slice)

def p_operator(p):
	''' operator : EQUALS_COMP
		| GREATER_EQUAL_OP
		| LESS_EQUAL_OP
		| LESS_THAN
		| GREATER_THAN
		| LESSEQUAL
		| NOTEQUAL
		| OR_OP
		| AND_OP '''
	lis.append(p.slice)

def p_if_else_block(p):
	''' if_else_block : if_block ELSE BEGIN_BLOCK stmts END_BLOCK '''
	lis.append(p.slice)

def p_else_if_block(p):
	''' else_if_block : if_block ELSE if_block ELSE BEGIN_BLOCK stmts END_BLOCK '''
	lis.append(p.slice)

def p_unsafe_block(p):
	''' unsafe_block : UNSAFE BEGIN_BLOCK stmts END_BLOCK '''
	lis.append(p.slice)

def p_match_block(p):
	''' match_block : MATCH ident BEGIN_BLOCK match_stmt END_BLOCK'''
	lis.append(p.slice)

def p_match_stmt(p):
	''' match_stmt : non_block_stmt mat non_block_stmt 
		| LIT_INTEGER mat non_block_stmt'''
	lis.append(p.slice)

def p_struct_block(p):
	''' struct_block : STRUCT ident BEGIN_BLOCK struct_stmt END_BLOCK '''
	lis.append(p.slice)

def p_struct_stmt(p):
	''' struct_stmt : ident COLON i32 '''
	lis.append(p.slice)
	

def p_error(p):
    if (hasattr(p,'type')):
        print "[Parsing] Error at line ",p.lineno,": Token:",p.type,"incorrectly parsed"

    global counter
    counter += 1
    if (counter > 10):
        sys.exit()

    parser.errok() 
    global success
    success = False


parser = yacc.yacc(start = 'compilation_unit', debug = True)



Debug = False

#Scanning the file name
parser = yacc.yacc(start = 'compilation_unit', debug = True)
if (len(sys.argv) == 1):
    file_name =raw_input( "Give a Rust file to parse: ")
else:
    file_name = sys.argv[1]

try:
	lexer = lex.lex()


	with open(file_name) as fp:#opening file
		data = fp.read()
		parser = yacc.yacc(start = 'compilation_unit', debug = True)
		lexer.input(data)
		result = parser.parse(data)
		fo = open("3ac.txt", "wb")
		for item in threeAC:
			print>>fo, item
		fo.close()
	
    	print success

   	    
except IOError as e:
    print "I/O error({0}): "+ "We are not able to open " + file_name + " . Does it Exists? Check permissions!"


