# advimport

## What is that

**advimport** is an alternative Python module import utility.

It handles missing modules and other things automatically.

## How do I use that
```
import advimport

advimport.import(module)
# same as doing 'import module'

advimport.import(module, subfunction1, subfunction2
# same as doing 'from main_module import subfunction2, subfunction2'
```

## Notes
This import helper sticks to PEP8, so it won't support:
* wildcard imports like `from module import *`
* multiple inline imports like `from module import this, that, those`
If you want to do those things, you'll have to use the built-in `import`
