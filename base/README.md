Weekly Python Challenge
======================

Welcome to the Weekly Python Challenge!
Every week a new example will be published here that you can try to solve.
At the end of the week, the solutions to the problem will be discussed over some coffee.

Overview
--------

The examples will be deposited into a folder named after `YEAR_WEEKNUMBER`. Please copy this folder
to a local drive and complete the exercises there. 

In the folder, there is an instruction file that explains the problem.
The `solution.py` file contains a `solution` function in which the problem should be solved.
The doc-string of the `solution` function will contain the examples that are in the instructions.

If the `solution.py` file is executed, the examples in the doc-string will be tested.
The file will look like this:

```python
def solution(*args, **kwds):
    """"This is the doc-string, this shortly 
    introduces what the function is supposed to do.

    :Examples:
    >>> solution(test_input)
    expected_output

    """"
    # place your solution here
    raise NotImplementedError


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
```

The `args` will be a list containing all positional arguments, `kwds` will be a dictionary 
containing all keyword arguments.
You can replace these parameters if you want, e.g. your example only requires one input.

The last three lines will only be exectured if the file is run directly, but not when it is imported
as a module.
