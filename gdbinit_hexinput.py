import gdb
import os

baseIOCTL = "(int)ioctl(open(\"{}\",1),0x5412,\"{}\")"


def shell_unhexlify(hex_arg, padding=0):
    if padding != 0:
        unhexlifed = r"\x" + r"\x".join(hex_arg[n: n+2]
                                    for n in range(0, len(hex_arg), 2))
    else:
        unhexlifed = r"\x" + r"\x".join(hex_arg[n: n+2]
                                        for n in range(0, len(hex_arg), 2)[::-1])
    unhexlifed += "\\x00" * (padding//8 - (len(unhexlifed) // 4))
    return unhexlifed


def hexinput(arg, padding=0):
    procs = gdb.selected_inferior()
    arg = shell_unhexlify(arg.replace(
        "0x", "").replace("\n", ""), padding) + "\\x0a"
    pid = procs.pid
    with open('/dev/stdout') as fd:
        tty_path = os.ttyname(fd.fileno())
    emit_str = baseIOCTL.format(tty_path, "c") + \
        " + " + baseIOCTL.format(tty_path, "\\n")
    for i in range(0, len(arg), 4):
        emit_str += " + " + baseIOCTL.format(tty_path, arg[i: i+4])
    emit_str = "call (void)(" + emit_str + ")"
    SILENT = True
    gdb.execute(emit_str)


class COMMAND_HexInput(gdb.Command):
    def __init__(self):
        super(COMMAND_HexInput, self).__init__(
            "hexinput", gdb.COMMAND_RUNNING | gdb.COMMAND_USER)
        self.last_pad_bits = 0

    def invoke(self, arg, from_tty):
        argv = arg.split(" ")
        hexnum = str(argv[0])
        if "big" in arg:
            hexinput(hexnum)
            return
        if len(argv) > 1:
            pad_bits = int(argv[1])
            self.last_pad_bits = pad_bits
            hexinput(hexnum, pad_bits)
        else:
            hexinput(hexnum, self.last_pad_bits)


COMMAND_HexInput()
