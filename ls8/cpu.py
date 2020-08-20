"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001


class CPU:
    """Main CPU class."""
    # create handle methods, takes operand as a param

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        self.running = True
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def handle_LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def handle_HLT(self, a, b):
        self.running = False

    def handle_PRN(self, a, b):
        # reg_num = self.ram_read(self.pc + 1)
        print(self.reg[a])

    def handle_ADD(self, a, b):
        self.alu("ADD", a, b)

    def handle_MUL(self, a, b):
        self.alu("MUL", a, b)

    def handle_PUSH(self, a, b):
        self.reg[7] -= 1
        register = self.ram_read(self.pc + 1)
        value = self.reg[register]
        sp = self.reg[7]
        self.ram[sp] = value

    def handle_POP(self, a, b):
        sp = self.reg[7]
        register = self.ram_read(self.pc + 1)
        value = self.ram[sp]
        self.reg[register] = value
        self.reg[7] += 1

    def handle_CALL(self, a, b):
        reg = self.ram_read(self.pc + 1)
        address = self.reg[reg]
        return_address = self.pc + 2
        self.reg[7] -= 1
        sp = self.reg[7]
        self.ram[sp] = return_address
        self.pc = address

    def handle_RET(self, a, b):
        sp = self.reg[7]
        return_address = self.ram[rp]
        self.reg[7] += 1
        self.pc = return_address

    def load(self, file_name):
        """Load a program into memory."""

        address = 0

        try:
            with open(file_name) as file:
                for line in file:
                    split_line = line.split('#')[0].strip()
                    if split_line == "":
                        continue
                    instructions = int(split_line, 2)
                    self.ram[address] = instructions
                    address += 1
        except FileNotFoundError:
            print(f"Not Found booiii")
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "PRN":
            self.handle_PRN(reg_a)
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while self.running:
            # print("running")
            # Instruction Register #missing Operand a/b
            ir = self.ram_read(self.pc)
            ir2 = self.ram_read(self.pc + 1)
            ir3 = self.ram_read(self.pc + 2)
            # value = ir
            # op_count = value >> 6
            # ir_length = 1 + op_count
            self.branchtable[ir](ir2, ir3)
            if ir != CALL and ir != RET:
                self.pc += (ir >> 6) + 1

            if ir == 0 or None:  # check instruction for print(PRN)
                print(f"Unknown Instruction: {ir}")
                # sys.exit()
