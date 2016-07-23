.data
t4:	.word 0
t2:	.word 0
t3:	.word 0
t1:	.word 0
.text
.globl main
main:
Loop1:
	 li $t9, -5
	 sw $t9, t1
	 li $t8, 10
	 sw $t8, t2
	 li $t3, 4
	 sw $t3, t3
	 lw $t8 , t2
	 lw $t9 , t1
	 lw $t9, t2
	 lw $t3, t3
	 div $t9, $t3
	 mfhi $t8
	 mflo $t9
	 sw $t9, t4
	 lw $t8, t4
	 sw $t8, t1
	 li $v0, 1
	 move $a0, $t8
	 syscall 
 	li $v0, 10
 	syscall
