from cx_Freeze import setup, Executable

base = None    

executables = [Executable("main.py", base=base)]

packages = ["frames"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "tureng",
    options = options,
    version = "0.01",
    description = 'Turengcli',
    executables = executables
)
