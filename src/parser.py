from three_addrcode_functions import *
from copy import deepcopy

import ply.yacc as yacc, sys
import subprocess
from lexer import tokens, lexer
import re

lis = []
lis2 =[]

success = True

def p_compilation_unitt(p):
	''' compilation_unit : ProgramFile '''
	

def p_ProgramFile(p):
	''' ProgramFile : main_fun
		| fun_def 
		| fun_def main_fun'''	
	p[0]=p[1]
	global success
	if success : symbol_table.print_Symbol_Table()

	if (Debug1) : print "Rule Done: 1"

def p_main_fun(p):
	''' main_fun : FN MAIN_FUN OPEN_PARANTHESIS CLOSE_PARANTHESIS BEGIN_BLOCK stmts END_BLOCK '''
	lis.append(p.slice)

def p_fun_def(p):
	''' fun_def : FN ident OPEN_PARANTHESIS arguments CLOSE_PARANTHESIS BEGIN_BLOCK stmts END_BLOCK
		| FN ident OPEN_PARANTHESIS CLOSE_PARANTHESIS BEGIN_BLOCK stmts END_BLOCK'''
	lis.append(p.slice)


def p_stmts(p):
	''' stmts : non_block_stmt
		| non_block_stmt stmts
		| block_stmt 
		| block_stmt stmts '''
	lis.append(p.slice)

def p_non_block_stmt(p):
	''' non_block_stmt : LET ident ASSIGNMENT_OP SENTENCE SEMICOLON
		| LET ident ASSIGNMENT_OP LIT_INTEGER SEMICOLON
		| LET ident ASSIGNMENT_OP LIT_FLOAT SEMICOLON
		| LET ident ASSIGNMENT_OP TRUE SEMICOLON
		| LET ident ASSIGNMENT_OP FALSE SEMICOLON
		| LET MUT ident ASSIGNMENT_OP LIT_INTEGER SEMICOLON
		| LET MUT ident ASSIGNMENT_OP LIT_FLOAT SEMICOLON
		| LET MUT ident ASSIGNMENT_OP TRUE SEMICOLON
		| LET MUT ident ASSIGNMENT_OP FALSE SEMICOLON
		| PRINT OPEN_PARANTHESIS SENTENCE CLOSE_PARANTHESIS SEMICOLON 
		| binop
		| bitop
		| fn_call '''
	lis.append(p.slice)

def p_binop(p):
	''' binop : ident ASSIGNMENT_OP ident next_ident SEMICOLON '''
	lis.append(p.slice)

def p_next_ident(p):
		''' next_ident : arith_op ident
			| arith_op ident next_ident '''	 
		lis.append(p.slice)


def p_arith_op(p):
	''' arith_op : PLUS
		| MINUS
		| MULTIPLICATION
		| DIVISION
		| MODULUS '''
	lis.append(p.slice)

def p_bitop(p):
	''' bitop : ident ASSIGNMENT_OP ident next_bit_ident SEMICOLON '''
	lis.append(p.slice)

def p_next_bit_ident(p):
	''' next_bit_ident : bit_op ident
		| bit_op ident next_bit_ident '''
	lis.append(p.slice)

def p_bit_op(p):
	''' bit_op : AND_LOGICAL
		| OR_LOGICAL
		| XOR_OP
		| NOT_OP
		| LEFT_SHIFT
		| RIGHT_SHIFT '''
	lis.append(p.slice)

def p_fn_call(p) :
	''' fn_call : ident OPEN_PARANTHESIS arguments CLOSE_PARANTHESIS SEMICOLON 
		| ident OPEN_PARANTHESIS CLOSE_PARANTHESIS SEMICOLON'''
	lis.append(p.slice)


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
	print "ERROR: error in parsing phase "+ str(p)
	lis.append(p.slice)

parser = yacc.yacc(start='compilation_unit')
#lis.reverse()

