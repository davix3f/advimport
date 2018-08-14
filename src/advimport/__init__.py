from os import system as shell
from os import path
import sys
import re

sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '.')))

from __pipfix_f__ import pipfix_f


__main_globals__ = None


def advimport_init(main_globals_arg):
    if type(main_globals_arg) is not dict:
        raise ValueError("Argument must be \'dict\'")
    global __main_globals__
    __main_globals__ = main_globals_arg


def advimport(main_module, *other_modules, name=None, pipfix=False, log=False):

    def pipfix_caller(module_target=main_module, values=pipfix):
        if type(values) in (list, tuple):
            try:
                #print("Calling pipfix_f with askconfirm", pipfix[0], "and automateinstall", pipfix[1])
                pipfix_f(module=module_target,
                         askconfirm=pipfix[0],
                         automate_install=pipfix[1])
            except:
                #print("Calling pipfix_f with askconfirm", pipfix[0])
                pipfix_f(module=module_target,
                         askconfirm=pipfix[0])

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
        if type(pipfix) in (tuple, list):
            if len(pipfix) > 2:
                raise ValueError("When pipfix is a tuple, it must contain\
                                 maximum two variables of type <bool> or <int>")
            if any(type(item) not in (bool,int) for item in pipfix):
                raise ValueError("When pipfix is a tuple, it must contain\
                                 maximum two variable of type <bool> or <int>")
        else:
            raise ValueError("pipfix must be <bool> or <tuple>|<list>(<bool>/<int>,<bool>/<int>)")

# Function to install missing modules using pip[pyversion being used]

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
                    if type(pipfix) is tuple:
                        pipfix_caller()
                        # use pipfix argument #1 as askconfirm value
                        #                     #2 as automateinstall value
                    else:
                        pipfix_f(main_module)
                        # run pipfix_f normally, askconfirm=True

# Import just main_module

    elif len(other_modules) is 0:
        try:
            __main_globals__[main_module if name==None else name] = __import__(main_module)
        except ImportError as ERROR:
            print("AdvancedImportError:",
                  re.search(r"named (?P<missing_module>\'.+\')",
                            ERROR.args[0]).group("missing_module"),
                  "does not exists or it is not installed")
            if pipfix:
                if type(pipfix) is tuple:
                    pipfix_caller()
                    # use pipfix argument #1 as askconfirm value
                    #                     #2 as automateinstall value
                else:
                    pipfix_f(main_module)
    else:
        raise ValueError("Invalid syntax")
