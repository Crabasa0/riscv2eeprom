#Compile a risc-v program into a circuitverse EEPROM
import sys
import json
import copy
import pyperclip
from compiler_data import registers, opcodes, func3, func7, EEPROM_template

text_instructions = []

#read the code into an array
for line in sys.stdin:
    text_instructions.append(line.strip())

#convert the text instructions into machine code and store in array
mc_instructions = []
for instr in text_instructions:
    #to lowercase
    instr = instr.lower()
    #get opcode text
    opcode_text = instr.split(" ")[0]
    params = ''.join(instr.split(' ')[1:]).split(',')
    if opcode_text[-1] == 'i' or opcode_text[0] == 'b':
        #this is an I-type instruction
        rd_text = params[0]
        rs1_text = params[1]
        imm_text = params[2]
        #convert registers into mc
        rd = registers[rd_text]
        rs1 = registers[rs1_text]
        imm = int(imm_text)
        #get mc opcode and func bits
        opcode_mc = opcodes[opcode_text]
        f3 = func3[opcode_text]
        #assemble mc instruction
        rd = rd << 7
        f3 = f3 << 12
        rs1 = rs1 << 15
        imm = imm << 20
        mc_instr = opcode_mc | rd | f3 | rs1 | imm
        mc_instructions.append(mc_instr)
    elif opcode_text == 'lw':
        #This is also I-type, but it requires special parsing
        rd_text = params[0]
        addr_text = params[1]
        addr_parts = addr_text.split('(')
        offset = int(addr_parts[0])
        base_reg = addr_parts[1][:-1]
        #convert registers, opcode, func3 to mc
        rd = registers[rd_text]
        rs1 = registers[base_reg]
        opcode_mc = opcodes[opcode_text]
        f3 = func3[opcode_text]
        imm = offset
        #assemble mc instruction
        rd = rd << 7
        f3 = f3 << 12
        rs1 = rs1 << 15
        imm = imm << 20
        mc_instr = opcode_mc | rd | f3 | rs1 | imm
        mc_instructions.append(mc_instr)
    elif opcode_text == 'sw':
        #this is an S-type instruction
        rs2_text = params[0]
        addr_text = params[1]
        addr_parts = addr_text.split('(')
        offset = int(addr_parts[0])
        base_reg = addr_parts[1][:-1]
        #convert registers, opcode, func3 to mc
        rs2 = registers[rs2_text]
        rs1 = registers[base_reg]
        opcode_mc = opcodes[opcode_text]
        f3 = func3[opcode_text]
        #split up the immediate value
        imm = offset
        imm_msb = imm >> 5
        lsb_mask = 0b000000011111
        imm_lsb = imm & lsb_mask
        #assemble the mc instruction
        imm_lsb = imm_lsb << 5
        f3 = f3 << 12
        rs1 = rs1 << 15
        rs2 = rs2 << 20
        imm_msb = imm_msb << 25
        mc_instr = opcode_mc | imm_lsb | f3 | rs1 | rs2 | imm_msb
        mc_instructions.append(mc_instr)
    else:
        #this is an R-type instruction
        rd_text = params[0]
        rs1_text = params[1]
        rs2_text = params[2]
        #convert the registers into mc
        rd = registers[rd_text]
        rs1 = registers[rs1_text]
        rs2 = registers[rs2_text]
        #get the mc opcode and func bits
        opcode_mc = opcodes[opcode_text]
        func3_mc = func3[opcode_text]
        func7_mc = func7[opcode_text]
        #assemble into a machine code instruction
        rd = rd << 7
        func3_mc = func3_mc << 12
        rs1 = rs1 << 15
        rs2 = rs2 << 20
        func7_mc = func7_mc << 25
        mc_instr = opcode_mc | rd | func3_mc | rs1 | rs2 | func7_mc
        mc_instructions.append(mc_instr)

#insert mc instructions into the EEPROM JSON
eeprom = copy.deepcopy(EEPROM_template)
data = eeprom['EEPROM'][0]['customData']['constructorParamaters'][3]
for i in range(len(mc_instructions)):
    data[3 * i] = mc_instructions[i]
pyperclip.copy(json.dumps(eeprom))
print(json.dumps(eeprom))
