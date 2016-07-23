import sys
import os

if len(sys.argv) == 2:
	filename = str(sys.argv[1])
else:
	print("usage: python 3ac.py testfile")
	exit()

reg = {'$t0' : None, '$t1' : None, '$t2' : None, '$t3' : None, '$t4' : None, '$t5' : None, 
	'$t6' : None, '$t7' : None, '$t8' : None, '$t9' : None}


operators = ['+', '-', '*', '/', '=', "ifgoto", "call", "ret", "label", "goto", "print", '==', '<=', '>=', '>', '<', '&', '|', "&&", "||", "!=", '!']

address = {}
varlist = []
mipsout = ""

def integer(number):
	if number.isdigit() or ( (number[0] == '+' or number[0] == '-') and number[1:].isdigit() ):
		return 1
	else:
		return 0

def getreg(variable):
	if variable in reg.values():
		for x in reg.keys():
			if reg[x] == variable:
				return x
	for x in reg.keys():
		if reg[x] == None:
			return x
	instrvar = nextuseTable[instrno - 1]
	farthestnextuse = max(instrvar.keys())
	for var in instrvar:
		if instrvar[var] == farthestnextuse:
			break;
	
	for regSpill in reg.keys():
		if reg[regSpill] == var:
			break;
	mipsout = mipsout + '\t lw ' + regSpill + ' , ' + var + '\n'
	return regSpill
	


def freereg(regName):
	if(reg[regName] != None):
		mipsout = '\t lw ' + regName + ' , ' + reg[regName] + '\n'
		reg[regName] = 'Memory'
		reg[regName] = None
		return mipsout

def prodMips(ins):
	mipsout=""
	lineNo=int(ins[0])
	
	operator = ins[1]
	if not operator in operators:
		print "operator ",operator," is not supported."

	elif operator == '+':
		dest = ins[2]
		operand1=ins[3]
		operand2=ins[4]		
		if integer(operand1) and integer(operand2):
			destreg=getreg(dest)
			mipsout=mipsout + "\t li " + destreg + ", " + operand1 + "\n"
			reg[destreg]=int(operand1)
		   	mipsout= mipsout + "\t addi " + destreg + ", " + destreg + ", " + operand2 + "\n"
			reg[destreg]=reg[destreg]+int(operand2)

		elif not integer(operand1) and not integer(operand2):
			destreg=getreg(dest)
			regop2 = getreg(operand2)
			reg[regop2]=operand2
			mipsout = mipsout + "\t lw " + destreg + " , " + operand1 + "\n"
			reg[destreg]=operand1
			mipsout = mipsout + "\t lw " + regop2 + " , " + operand2 + "\n"
			mipsout = mipsout + "\t add " + destreg + " , " + destreg + " , " + regop2 + "\n"
			reg[destreg]= dest

		elif not integer(operand1) and integer(operand2):
		   	destreg=getreg(dest)
		   	mipsout = mipsout + "\t lw " + destreg + " , " + operand1 + "\n"
		   	reg[destreg]=operand1
		   	mipsout = mipsout + "\t add " + destreg + " , " + destreg + " , " + operand2 + "\n"
		   	reg[destreg]= dest

		else:
		   	destreg=getreg(dest)
		   	mipsout = mipsout + "\t lw " + destreg + " , " + operand2 + "\n"
		   	reg[destreg]=operand2
		   	mipsout = mipsout + "\t add " + destreg + " , " + destreg + " , " + operand1 + "\n"
		   	reg[destreg]= dest

		mipsout = mipsout + "\t sw " + destreg + " , " + dest + "\n"

	elif operator == '-':

	 	dest = ins[2]
		operand1 = ins[3]
		operand2 = ins[4]
		if integer(operand1) and integer(operand2):
		   	destreg=getreg(dest)
		   	regop2 = getreg(operand2)
		   	reg[regop2]=operand2
		   	mipsout = mipsout + "\t li " + destreg + ", " + operand1 + "\n"
		   	reg[destreg]=operand1
		   	mipsout = mipsout + "\t li " + regop2 + ", " + operand2 + "\n"
		   	mipsout = mipsout + "\t sub " + destreg + ", " + destreg + ", " + regop2 + "\n"
		   	reg[destreg]= dest 

		elif not integer(operand1) and not integer(operand2):
		   	destreg=getreg(dest)
		   	regop2 = getreg(operand2)
		   	reg[regop2]=operand2
		   	mipsout = mipsout + "\t lw " + destreg + ", " + operand1 + "\n"
		   	reg[destreg]=operand1
		   	mipsout = mipsout + "\t lw " + regop2 + ", " + operand2 + "\n"
		   	mipsout = mipsout + "\t sub " + destreg + ", " + destreg + ", " + regop2 + "\n"
		   	reg[destreg]= dest

		elif not integer(operand1) and integer(operand2):
		   	destreg=getreg(dest)
		   	regop2 = getreg(operand2)
		   	reg[regop2]=operand2
		   	mipsout = mipsout + "\t lw " + destreg + ", " + operand1 + "\n"
		   	reg[destreg]=operand1
		   	mipsout = mipsout + "\t li " + regop2 + ", " + operand2 + "\n"
		   	mipsout = mipsout + "\t sub " + destreg + ", " + destreg + ", " + regop2 + "\n"
		   	reg[destreg]= dest

		else:
		   	destreg=getreg(dest)
		   	regop2 = getreg(operand2)
		   	mipsout = mipsout + "\t lw " + regop2 + ", " + operand2 + "\n"
		   	reg[regop2]=operand2
		   	mipsout = mipsout + "\t li "+ destreg + ", " + operand1 + "\n"
		   	mipsout = mipsout + "\t sub " + destreg + ", " + destreg + ", " + regop2 + "\n"
		   	reg[destreg]= dest

		mipsout = mipsout + "\t sw " + destreg + ", " + dest + "\n"

	elif (operator == '/'):
		quotient = ins[2]
		operand1 = ins[3]
		operand2 = ins[4]

		if reg['$t8'] != None: 
		   	mipsout = mipsout + freereg('$t8')
		if reg['$t9'] != None:
		   	mipsout = mipsout + freereg('$t9')
		
		div = getreg(operand1)
		if integer(operand1):
		   	mipsout = mipsout + "\t li " + div + ", " + operand1 + "\n"
		   	reg[div]=int(operand1)
		else:
		   	mipsout = mipsout + "\t lw " + div + ", " + operand1 + "\n"
		   	reg[div]=operand1
		regop2 = getreg(operand2)
		if integer(operand2):
		   	mipsout = mipsout + "\t li " + regop2 + ", " + operand2 +"\n"
		   	reg[regop2]=int(operand2)
		else:
		   	mipsout = mipsout + "\t lw " + regop2 + ", "+ operand2 + "\n"
		   	reg[regop2]=operand2

		mipsout = mipsout + "\t div " + div + ", " + regop2 + "\n"
		mipsout = mipsout + "\t mfhi $t8\n"
		mipsout = mipsout + "\t mflo $t9\n"
		mipsout = mipsout + "\t sw $t9, " + quotient + "\n"

		if integer(operand1) and integer(operand2):
			reg['$t9'] = operand1 / operand2
			reg['$t8'] = operand1 % operand2
		else:
			reg['$t9'] = quotient

	elif operator == '*':
	       	dest = ins[2]
		operand1 = ins[3]
		operand2 = ins[4]

		if integer(operand1) and integer(operand2):
		   	destreg=getreg(dest)
		   	mipsout = mipsout + "\t li " + destreg + ", " + operand1 + "\n"
		   	reg[destreg]=operand1
		   	regop2 = getreg(operand2)
		   	mipsout = mipsout + "\t li " + regop2 + ", " + operand2 + "\n"
		   	reg[regop2]=int(operand2)
		   	mipsout= mipsout + "\t mult " + destreg +", " + regop2 + "\n"
		   	reg[destreg] = int(operand1) * int(operand2)

		elif not integer(operand1) and not integer(operand2):
		   	destreg=getreg(dest)
		   	regop2 = getreg(operand2)
		   	reg[regop2]=operand2
		   	mipsout = mipsout + "\t lw " + destreg + ", " + operand1 + "\n"
		   	reg[destreg]=operand1
		   	mipsout = mipsout + "\t lw " + regop2 + ", " + operand2 + "\n"
		   	mipsout = mipsout + "\t mult " + destreg + ", " + regop2 + "\n"
		   	reg[destreg]= dest 

		elif not integer(operand1) and integer(operand2):
		   	destreg=getreg(dest)
		   	mipsout = mipsout + "\t lw " + destreg + ", " + operand1 + "\n"
		   	reg[destreg]=operand1
		   	regop2 = getreg(operand2)
		   	mipsout = mipsout + "\t li " + regop2 + ", " + operand2 + "\n"
		   	reg[regop2]=int(operand2)
		   	mipsout= mipsout + "\t mult " + destreg +", " + regop2 + "\n"
		   	reg[destreg]= dest

		else:
		   	destreg=getreg(dest)
		   	regop2 = getreg(operand2)
		   	mipsout = mipsout + "\t lw " + regop2 + ", " + operand2 + "\n"
		   	reg[regop2]=operand2
		   	mipsout = mipsout + "\t li "+ destreg + ", " + operand1 + "\n"
		   	mipsout = mipsout + "\t mult " + destreg + ", " + regop2 + "\n"
		   	reg[destreg]= dest
 
		mipsout = mipsout + "\t mfhi $t8\n"
		mipsout = mipsout + "\t mflo " + destreg + "\n"
 		mipsout = mipsout + "\t sw " + destreg + " , " + dest + "\n"

	elif operator == "=":
		dest = ins[2]
		src = ins[3]
		destreg=getreg(dest)
		reg[destreg]= dest
		if integer(src):
		   	mipsout = mipsout + "\t li "+ destreg +", " + src +'\n'
		   	reg[destreg]=src
		else:
		   	mipsout = mipsout + "\t lw "+ destreg +", "+ src +'\n'
		   	reg[destreg]=src

		mipsout = mipsout + "\t sw " + destreg + ", "+ dest +'\n'
		reg[destreg]=dest



	elif operator == "ifgoto":
		operatorin = ins[2]

		if operatorin =="==" or operatorin==">=" or operatorin == "<=" or operatorin == ">" or operatorin == "<" or operatorin == "!=":
			operand1 = ins[3]
			operand2 = ins[4]
		        gotoloc = ins[5]
			if integer(operand1) and integer(operand2):
			  	destreg=getreg(operand1)
			   	mipsout = mipsout + "\t li " + destreg + ", " + operand1 + "\n"
			   	reg[destreg]=int(operand1)
			   	mipsout= mipsout + "\t cmpq " + destreg + " , " + operand2 + "\n"
			   	reg[destreg]=operand1

			elif not integer(operand1) and not integer(operand2):
			   	destreg=getreg(operand1)
			   	regop2 = getreg(operand2)
			   	reg[regop2]=operand2
			   	mipsout = mipsout + "\t lw " + destreg + "," + operand1 + "\n"
			   	reg[destreg]=operand1
			   	mipsout = mipsout + "\t lw " + regop2 + "," + operand2 + "\n"
			   	mipsout = mipsout + "\t cmpq " + destreg + "," + regop2 + "\n"
			   	reg[destreg]= operand1 

			elif not integer(operand1) and integer(operand2):
			   	destreg=getreg(operand1)
			   	mipsout = mipsout + "\t lw " + destreg + "," + operand1 + "\n"
			   	reg[destreg]=operand1
			   	mipsout = mipsout + "\t cmpq " + destreg + "," + operand2 + "\n"
			   	reg[destreg]= operand1

			else:
			   	destreg=getreg(operand2)
			   	mipsout = mipsout + "\t lw " + destreg + "," + operand2 + "\n"
			   	reg[destreg]=operand2
			   	mipsout = mipsout + "\t cmpq " + destreg + "," + operand1 + "\n"
			   	reg[destreg]= operand1

			if operatorin == "==":
			   	mipsout=mipsout+"\t be Loop"+gotoloc +"\n"

			elif operatorin == "<=":
			   	mipsout=mipsout+"\t ble  Loop"+gotoloc +"\n"

                        elif operatorin == "<":
			   	mipsout=mipsout+"\t blt  Loop"+gotoloc +"\n"
				   
			elif operatorin == ">=":
			   	mipsout=mipsout+"\t bge  Loop"+gotoloc +"\n"
				
			elif operatorin == ">":
			   	mipsout=mipsout+"\t bgt  Loop"+gotoloc +"\n"
				
			elif operatorin == "!=":
			   	mipsout=mipsout+"\t bne  Loop"+gotoloc +"\n"

			
		elif operatorin == '&&'or operatorin == '&' :

		  	operand1 = ins[3]
		   	operand2 = ins[4]
		   	gotoloc = ins[5]

			if integer(operand1) and integer(operand2):
				destreg=getreg(operand1)
				mipsout = mipsout + "\t li " + destreg + ", " + operand1 + "\n"
				reg[destreg]=int(operand1)
				mipsout= mipsout + "\t and " + destreg +", " + operand2 + "\n"
				reg[destreg]=operand1
			elif not integer(operand1) and not integer(operand2):
			   	destreg=getreg(operand1)
			   	regop2 = getreg(operand2)
			   	reg[regop2]=operand2
			   	mipsout = mipsout + "\t lw " + destreg + "," + operand1 + "\n"
			   	reg[destreg]=operand1
			   	mipsout = mipsout + "\t lw " + regop2 + "," + operand2 + "\n"
			   	mipsout = mipsout + "\t and " + destreg + "," + regop2 + "\n"
			   	reg[destreg]= operand1 
			elif not integer(operand1) and integer(operand2):
				destreg=getreg(operand1)
				mipsout = mipsout + "\t lw " + destreg + "," + operand1 + "\n"
				reg[destreg]=operand1
				mipsout = mipsout + "\t and " + destreg + "," + operand2 + "\n"
				reg[destreg]= operand1
			else:
				destreg=getreg(operand2)
				mipsout = mipsout + "\t lw " + destreg + "," + operand2 + "\n"
				reg[destreg]=operand2
				mipsout = mipsout + "\t and " + destreg + "," + operand1 + "\n"
				reg[destreg]= operand1
				mipsout=mipsout+"\t jnz  Loop"+gotoloc +"\n"


		elif operatorin == '||' or operatorin == '|':

			operand1 = ins[3]
	   		operand2 = ins[4]
	 		gotoloc = ins[5]

			if (integer(operand1) and integer(operand2)):
		   		destreg=getreg(operand1)
		   		mipsout = mipsout + "\t li " + destreg + ", " + operand1 + "\n"
		   		reg[destreg]=int(operand1)
		   		mipsout= mipsout + "\t or " + destreg +", " + operand2 + "\n"
		   		reg[destreg]=operand1
			elif not integer(operand1) and not integer(operand2):
				destreg=getreg(operand1)
				regop2 = getreg(operand2)
				reg[regop2]=operand2
				mipsout = mipsout + "\t lw " + destreg + "," + operand1 + "\n"
				reg[destreg]=operand1
				mipsout = mipsout + "\t lw " + regop2 + "," + operand2 + "\n"
				mipsout = mipsout + "\t or " + destreg + "," + regop2 + "\n"
				reg[destreg]= operand1 
			elif not integer(operand1) and integer(operand2):
				destreg=getreg(operand1)
			   	mipsout = mipsout + "\t lw " + destreg + "," + operand1 + "\n"
			   	reg[destreg]=operand1
			   	mipsout = mipsout + "\t or " + destreg + "," + operand2 + "\n"
				reg[destreg]= operand1
			else:
				destreg=getreg(operand2)
				mipsout = mipsout + "\t lw " + destreg + "," + operand2 + "\n"
				reg[destreg]=operand2
				mipsout = mipsout + "\t or " + destreg + "," + operand1 + "\n"
				reg[destreg]= operand1

			mipsout = mipsout+"\t jnz  Loop"+ gotoloc +"\n"


		elif operatorin == '!':

			operand1 = ins[3]
            	        gotoloc = ins[4]

		        destreg = getreg(operand1) 
		        if integer(operand1):
		          	mipsout = mipsout + "\t li " + destreg + " , " + operand1 + "\n"
				mipsout = mipsout + "\t bne " + destreg + "\n"
			else:
			   	mipsout = mipsout + "\t lw " + destreg + " , " + dest + "\n"
				mipsout = mipsout + "\t bne " + destreg + "\n"
			reg[destreg]=operand1
			mipsout=mipsout+"\t jnz  Loop"+gotoloc +"\n"


	elif operator == "label":
	 	funcstart = ins[2]
		mipsout = mipsout +  funcstart + ":\n\t mfhi $t1\n \t lw $t0, $t1\n"


	elif operator == "goto":
		destloc = ins[2]
		mipsout = mipsout + "\t j  Loop" + destloc + "\n"

	elif operator == "call":
		func = ins[2]
		mipsout = mipsout + "\t syscall " + func + '\n'
		mipsout = mipsout + "\t add $0, %rsp\n"


	elif operator == "print":
		printvar=ins[2]
		if integer(printvar):
			printreg=getreg(printvar)
			mipsout = mipsout + "\t li $v0, 1\n"
			mipsout = mipsout + "\t move $a0, " + printreg +  "\n"
			mipsout = mipsout + "\t syscall \n"		
		else:
			printreg = getreg(printvar)
			mipsout = mipsout + "\t li $v0, 1\n"
			mipsout = mipsout + "\t move $a0, " + printreg +  "\n"
			mipsout = mipsout + "\t syscall \n"


	elif operator == 'ret':
	 	mipsout = mipsout + "\t lw $t0, $t1\n\t popl $t0 \n\t ret \n"

	return mipsout




testfile = open(filename, 'r')
testcode = testfile.read()
testcode = testcode.strip('\n')

instrlist = []
instrlist = testcode.split('\n')


nextuseTable = [None for i in range(len(instrlist))]


for instr in instrlist:
	templist = instr.split(', ')
	if templist[1] not in ['label', 'call', 'function']:
		varlist = varlist + templist 

varlist = list(set(varlist))

varlist = [x for x in varlist if not integer(x)]


for word in operators:
	if word in varlist:
		varlist.remove(word)


address = address.fromkeys(varlist, "stat")

symbolTable = address.fromkeys(varlist, ["live", None])

leaders = [1,]
for i in range(len(instrlist)):
	instrlist[i] = instrlist[i].split(', ')
	
	if 'ifgoto' in instrlist[i]:
		leaders.append(int(instrlist[i][-1]))
		leaders.append(int(instrlist[i][0])+1)
		
	elif 'goto' in instrlist[i]:
		leaders.append(int(instrlist[i][-1]))
		leaders.append(int(instrlist[i][0])+1)

	elif 'function' in instrlist[i]:
		leaders.append(int(instrlist[i][0]))

	elif 'label' in instrlist[i]:
		leaders.append(int(instrlist[i][0]))

leaders = list(set(leaders))
leaders.sort()


nodes = []
i=0
for i in range(len(leaders)-1):
	nodes.append(list(range(leaders[i],leaders[i+1])))
	i = i + 1
nodes.append(list(range(leaders[i],len(instrlist)+1)))



for node in nodes:
	block=node
	for segment in block:
		instr = instrlist[segment - 1]
		operator = instr[1]

		variables = [x for x in instr if x in varlist]

		nextuseTable[segment-1] = { var : symbolTable[var] for var in varlist }	
		
		if operator in ['+','-','*','/']:
			z = instr[2]
			x = instr[3]
			y = instr[4]
			if z in variables:
				symbolTable[z] = ["dead", None]
			if x in variables:
				symbolTable[x] = ["live", segment]
			if y in variables:
 				symbolTable[y] = ["live", segment]

	  	elif operator == "ifgoto":
			x = instr[3]
			y = instr[4]
			if x in variables:
				symbolTable[x] = ["live", segment]
			if y in variables:
				symbolTable[y] = ["live", segment]

		elif operator == "print":
			x = instr[2]
			if x in variables:
				symbolTable[x] = ["live", segment]			

		elif operator == "=":
			x = instr[2]
			y = instr[3]
			if x in variables:
				symbolTable[x] = ["dead", None]
			if y in variables:
				symbolTable[y] = ["live", segment]					
			i = i - 1

data_section = '.data\n'
for var in varlist:
	data_section = data_section + var + ":\t" + ".word 0" + "\n" 
#data_section = data_section +"format: \n\t .asciiz\n"


text_section = '.text\n'+'.globl main\n'+'main:\n'
for node in nodes:
	text_section = text_section + "Loop" + str(node[0]) + ":\n"
	for n in node:
		text_section = text_section + prodMips(instrlist[n-1])

Mips = data_section + text_section + " \tli $v0, 10\n" + " \tsyscall"


print(Mips)

