# Overview
This is extention for gdb in Linux.  
You can input any bytes via stdin.  

# installation  
add follwing line to .gdbinit  
```
source <path_to_gdbinit_hexinput.py>
```
# example  
```
(gdb)hexinput 11223344
```

```
(gdb-peda)hexinput 0x11223344
```

you can pack with nbytes
```
(gdb)hexinput 0xdeadbeef 8 #0xdeadbeef will be packed for 8bytes little endian
```
