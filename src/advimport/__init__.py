from os import system as shell
import re
from sys import version_info

def advimport(main_module, *other_modules, name=None, pipfix=False, log=False):

# Function to install missing modules using pip[pyversion being used]

    def pipfix_f(module=main_module, askconfirm=True):
        print("Trying to install", module, "using pip" + str(version_info[0]))
        if askconfirm:
            if input("Proceed? y/n: ") == "y":
                pass
            else:
                print("Aborted")
                return 1
        shell("pip" + str(version_info[0]) + " install --user " + module)

# Import submodules from main_module, with name assignments

    if len(other_modules) >= 1:
        if name is not None:
            raise ValueError("\'name\' has to be None if you are importing submodules. Use a dictionary")
        import_commands = []
        for item in other_modules:
            if type(item) is str:
                import_commands.append((main_module, item, item))
            elif type(item) is dict:
                for element in item:
                    import_commands.append((main_module, element, item[element]))
        try:
            for item in import_commands:
                globals()[item[2]] = getattr(__import__(item[0]), item[1])
                if log:
                    print("Imported", item[1], "from", item[0], "as", item[2])
        except AttributeError as ERROR:
            if "has no attribute" in ERROR.args[0]:
                print("AdvancedImportError:",re.search(r"attribute (?P<missing_submodule>\'\w+\')", ERROR.args[0]).group("missing_submodule"),\
                "is not a member of", main_module)
        except ImportError as ERROR:
            if "module named" in ERROR.args[0]:
                print("AdvancedImportError:",re.search(r"named (?P<missing_module>\'\w+\')", ERROR.args[0]).group("missing_module"),\
                "does not exists or it is not installed")
                if pipfix:
                    if type(pipfix) is tuple and len(pipfix) is 2:
                        pipfix_f(askconfirm=pipfix[1])
                    else:
                        pipfix_f()

# Import just main_module

    elif len(other_modules) is 0:
        try:
            globals()[main_module if name==None else name] = __import__(main_module)
        except ImportError as ERROR:
            print("AdvancedImportError:",re.search(r"named (?P<missing_module>\'\w+\')", ERROR.args[0]).group("missing_module"),\
            "does not exists or it is not installed")
            if pipfix:
                if type(pipfix) is tuple and len(pipfix) is 2:
                    pipfix_f(askconfirm=pipfix[1])
                else:
                    pipfix_f()
    else:
        raise ValueError("Invalid syntax")