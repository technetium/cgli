# cgli

A utility to use a python program from both command line (cli) as website (cgi)

## Installation

Use pip to install *cgli*

```
	pip install cgli
```

## Usage

Example script:

```python
# import the application_make 
# and application_execute functions
# from the cgli module
from cgli import application_maker, application_execute


# define the arguments
arguments = {
    'string'  : { 'short': 's', 'help': 'a string' },
    'number'  : { 'short': 'n', 'help': 'a number', 'type': int },
    'another' : { 'short': 'a', 'help': 'another number', 'default': 42, 'type': int },
}

# define a function with the arguments defined above
def some_function(string, number, another):
    # do something
    sum = number + another
    
    # return something
    return {
        'string': 'The string is %s' % string,
        'number': 'The number is %d' % number,
        'sum': sum,
    }
    

# make the application and execute it
application_execute(application_maker(some_function, arguments))
```

### Command line

Show arguments:
```$ ./example.py -h```
Use arguments (long and short attribute names can be combined):
```$ ./example.py -s"Hello World" --number 3```

###
Show arguments:
``` http://example.com/example.py?h```
Use arguments (only long attribute names can be used)
``` http://example.com/example.py?string=Hello+World&number=3```
