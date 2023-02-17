# Python Toolbox
This module is a collection of some tools that I've used in my python projects. I am planning to fill this collection as I go on in programming.

## [version_controller](https://github.com/bateni1380/PyToolBox/blob/main/DebuggerNotebook.ipynb)
This is a version controller like git hub but for variables.
First can instantiate an object of this class.
```python 
from pytoolbox.version_controller import VersionController
vc = VersionController()
```
Then you can simply assign a variable to this object:
```python 
vc.a = 10
```
And you can save changes whenever you want (it's similar to commit in github)
```python 
vc.make_check_point()
```
Now you have a version controller and you can use 
`vc.undo()` and `vc.redo()` to switch between versions.

You can see a full documentation [here](https://github.com/bateni1380/PyToolBox/blob/main/DebuggerNotebook.ipynb).


## [debugger](https://github.com/bateni1380/PyToolBox/blob/main/DebuggerNotebook.ipynb)

This class is a class to observe status of the code. 

You can create an instance of this class and whenever you want to print something to see the status of your code, you can use debugger.log(description: str) to print status.

This class provides you many tools in order to observe the status of you're program better.
```python 
from pytoolbox.debugger import Debugger
debugger = Debugger(textual_debug=True, show_line=True)
debugger.log_start('PHASE1')
debugger.log('PHASE2')      
debugger.log('PHASE3')
debugger.log_end()
del debugger
```
This code outputs the following answer:
```text
[line 1] Debugger init started 
	[line 2] PHASE1 started 
		[line 3] PHASE2 time = 0.0090
		[line 4] PHASE3 time = 0.0170
	[line 5] PHASE1 ended time = 0.0260
[line 6] Debugger init ended time = 0.0440
```
You can see a full documentation
[here](https://github.com/bateni1380/PyToolBox/blob/main/DebuggerNotebook.ipynb).

