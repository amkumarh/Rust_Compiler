#! /bin/bash
python irgen.py ~/Desktop/project/test/test1.rs
python mips.py 3ac.txt > mips.asm
spim -file mips.asm
