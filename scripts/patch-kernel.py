import os
import sys

kernel_dir = sys.argv[1] if len(sys.argv) > 1 else "."

# 1. Patch kernel/module.c for vendor module compatibility
mod_file = os.path.join(kernel_dir, "kernel/module.c")
if os.path.exists(mod_file):
    with open(mod_file, "r") as f:
        s = f.read()
    s = s.replace("goto bad_version;", "return 1;")
    s = s.replace("return strcmp(amagic, bmagic) == 0;", "return 1;")
    s = s.replace("return 0;\n}\n\nstatic inline int check_modstruct_version", "return 1;\n}\n\nstatic inline int check_modstruct_version")
    with open(mod_file, "w") as f:
        f.write(s)
    print("Patched kernel/module.c successfully")

# 2. Patch arch/arm64/kernel/process.c to always define and export __stack_chk_guard
proc_file = os.path.join(kernel_dir, "arch/arm64/kernel/process.c")
if os.path.exists(proc_file):
    with open(proc_file, "r") as f:
        s = f.read()
    s = s.replace("#ifdef CONFIG_CC_STACKPROTECTOR\n#include <linux/stackprotector.h>", "#include <linux/stackprotector.h>")
    s = s.replace("EXPORT_SYMBOL(__stack_chk_guard);\n#endif", "EXPORT_SYMBOL(__stack_chk_guard);")
    with open(proc_file, "w") as f:
        f.write(s)
    print("Patched arch/arm64/kernel/process.c successfully")

# 3. Patch kernel/panic.c to always define and export __stack_chk_fail
panic_file = os.path.join(kernel_dir, "kernel/panic.c")
if os.path.exists(panic_file):
    with open(panic_file, "r") as f:
        s = f.read()
    s = s.replace("#ifdef CONFIG_CC_STACKPROTECTOR\n\n/*", "/*")
    s = s.replace("EXPORT_SYMBOL(__stack_chk_fail);\n\n#endif", "EXPORT_SYMBOL(__stack_chk_fail);\n")
    with open(panic_file, "w") as f:
        f.write(s)
    print("Patched kernel/panic.c successfully")
