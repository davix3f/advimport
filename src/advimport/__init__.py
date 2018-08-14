from os import system as shell
import re
from sys import version_info

__main_globals__ = None


def advimport_init(main_globals_arg):
    if type(main_globals_arg) is not dict:
        raise ValueError("Argument must be \'dict\'")
    global __main_globals__
    __main_globals__ = main_globals_arg


def advimport(main_module, *other_modules, name=None, pipfix=False, log=False):

    if __main_globals__ is None:
        raise ValueError("advimport not initiated. \
                         Run advimport_init(globals()) first")
    if type(__main_globals__) is not dict:
        raise ValueError("Pass a variable of type <dict> to advimport_init()")
    if name is not None:
        if type(name) is not str:
            raise ValueError("\'name\' must be a string")
    if type(log) not in (bool, int):
        raise ValueError("\'log\' must be bool or int(1/0)")

    if type(pipfix) is not bool:
        if type(pipfix) is tuple:
            if len(pipfix) > 2:
                raise ValueError("When pipfix is a tuple, it must contain\
                                 only two variable of type <bool>, or 1/0")
            if (type(pipfix[0]) not in (bool, int)) or (type(pipfix[1]) not in (bool, int)):
                raise ValueError("When pipfix is a tuple, it must contain\
                                 only two variable of type <bool>")
        else:
            raise ValueError("pipfix must be <bool> or <tuple>(<bool>/1/0,<bool>/1/0)")

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
            raise ValueError("\'name\' has to be None if you are importing \
            submodules. Use a dictionary")
        import_commands = []
        for item in other_modules:
            if type(item) is str:
                import_commands.append((main_module, item, item))
            elif type(item) is dict:
                for element in item:
                    import_commands.append((main_module,  # big module
                                            element,  # original submodule name
                                            item[element]))  # submodule alias
        try:
            for item in import_commands:
                __main_globals__[item[2]] = getattr(__import__(item[0]), item[1])
                if log:
                    print("Imported", item[1], "from", item[0], "as", item[2])
        except AttributeError as ERROR:
            if "has no attribute" in ERROR.args[0]:
                print("AdvancedImportError:",
                      re.search(r"attribute (?P<missing_submodule>\'\w+\')",
                                ERROR.args[0]).group("missing_submodule"),
                      "is not a member of", main_module)
        except ImportError as ERROR:
            if "module named" in ERROR.args[0]:
                print("AdvancedImportError:",
                      re.search(r"named (?P<missing_module>\'\w+\')",
                                ERROR.args[0]).group("missing_module"),
                      "does not exists or it is not installed")
                if pipfix:
                    if type(pipfix) is tuple and len(pipfix) is 2:
                        pipfix_f(askconfirm=pipfix[1])
                        # use pipfix argument #1 as askconfirm value
                    else:
                        pipfix_f()
                        # run pipfix_f normally, askconfirm=True

# Import just main_module

    elif len(other_modules) is 0:
        try:
            __main_globals__[main_module if name==None else name] = __import__(main_module)
        except ImportError as ERROR:
            print("AdvancedImportError:",
                  re.search(r"named (?P<missing_module>\'\w+\')",
                            ERROR.args[0]).group("missing_module"),
                  "does not exists or it is not installed")
            if pipfix:
                if type(pipfix) is tuple and len(pipfix) is 2:
                    pipfix_f(askconfirm=pipfix[1])
                else:
                    pipfix_f()
    else:
        raise ValueError("Invalid syntax")
