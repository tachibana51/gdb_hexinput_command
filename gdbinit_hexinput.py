import gdb
import os 
baseIOCTL = "(int)ioctl(open(\"{}\",1),0x5412,\"{}\")"

def shell_unhexlify(hex_arg):
    unhexlifed = r"\x" + r"\x".join(hex_arg[n : n+2] for n in range(0, len(hex_arg), 2))
    return unhexlifed

def hexinput(arg):
    procs = gdb.selected_inferior()
    arg = shell_unhexlify(arg.replace("0x","").replace("\n","")) + "\\x0a"
    pid = procs.pid
    with open('/dev/stdout') as fd:
        tty_path = os.ttyname(fd.fileno())
    emit_str = baseIOCTL.format(tty_path, "c") +" + "+ baseIOCTL.format(tty_path, "\\n")
    for i in range(0, len(arg), 4):
        emit_str += " + " + baseIOCTL.format(tty_path, arg[i : i+4])
    emit_str  ="call (void)(" + emit_str + ")"
    SILENT=True
    gdb.execute(emit_str)

class COMMAND_HexInput(gdb.Command):
    def __init__(self):
        super(COMMAND_HexInput, self).__init__("hexinput", gdb.COMMAND_RUNNING | gdb.COMMAND_USER)
    def invoke(self, arg, from_tty):
        hexinput(arg)

COMMAND_HexInput()
