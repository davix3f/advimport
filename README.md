# advimport

### Simpler and better imports for everyone

## What is that

**advimport** is an alternative, more advanced and
automatically managed way to import modules in Python.

**Why?**
It handles missing modules automatically.

**I don't see any code here**
or
**The code here is old**

Check [dev](https://github.com/davix3f/advimport/tree/dev "/tree/dev") branch

## Notes
This import helper sticks to PEP8, so it won't support:
* wildcard imports like `from module import *`
* multiple inline imports like `import this, that, this_one_too`
* Others may come

If you want to do that, you'll have to use the built-in `import`

## Installation
This module can't hack into other people's PC
and self-install. Still, you can install it by running

`pip3 install --user advimport`

## Usage
```python
from advimport import advimport, advimport_init

advimport_init(globals())
# First, you need to set where your global variables are set

advimport("module")
# Same as 'import module'. Not really useful
# if you are importing a module which is part
# of the included Python library.

advimport("module", name="module_alias")
# Same as 'import module as module_alias'

advimport("big_module", {"submodule1":"submodule1_alias",
                         "submodule2":"submodule2_alias"})
# Same as
# 'from big_module import submodule1 as submodule1_alias, submodule2 as submodule2_alias'

advimport("big_module", "submodule1", "submodule2"...)
# Same as
# 'from big_module import submodule1, submodule2...'

# Those two syntaxes can be combined, like this
advimport("big_module", {"submodule1":"submodule1_alias"}, "submodule2")
# Same as
# 'from big_module import submodule1 as submodule1_alias, submodule2'
```

#### Optional arguments
* `<str>` **name**: alternative name for one single import. Set to *None* by default.
* `<tuple>`|`<list>`|`<bool>` **pipfix**: this is the core of advimport. This value is usually set to False, but if set to True, it will try to install the missing modules. Set to (False, True) to automatically start installation, without asking user confirmation.
* `<bool>` **log**: Set to *False* by default. If set as
True, the output will be more verbose.

```python
from advimport import advimport

advimport("main_not_included_module", "eventual_submodule", pipfix=(True,False))
# If the "main_not_included_module" module isn't installed,
# pip will try to install it. 'pipfix' is set as (True, False),
# so it means that it will ask for user confirm before installing
# the module. The second bool (False), means that you can choose
# which module to install after a pip search.
# By default, this second option is set as True.

advimport("main_not_included_module", "submodule", pipfix=True)
# This will run the automatic dependency-fixing with default values:
# Asking for user confirmation;
# Automatically selecting the package to install
```

## The module is not working as it should
Open an issue 🆘

## I fixed something or I'd like to contribute
Open a pull request 📥
