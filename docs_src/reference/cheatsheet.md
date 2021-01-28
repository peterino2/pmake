# Pmake Cheatsheet

So this thing should theoretically be easy enough to use with all the information needed for it on one cheatsheet.

## Specifying jobs

`pmake` will start parsing pmakefiles. Importing the root pmakefile as a python object and start registering jobs. Jobs are functions decorated with the `@job` decorator.

```{code} python
   @job("dependency1", "dependency2", desc="Can't think of a good description", default=True)
   def my_jobname():
        # ...
```

Dependencies are specified in a list, and all arguments to the `@job` decorator are optional.


