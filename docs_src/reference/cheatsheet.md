# Pmake Cheatsheet
So this thing should theoretically be easy enough to use with all the information needed for it on one cheatsheet.
You can invoke pogmake with either `pogmake` or `pog`. It'll do the same thing.

## Specifying jobs

`pogmake` will start parsing pogfiles. Importing the root pogfile as a python object and start registering jobs. Jobs are functions decorated with the `@job` decorator.

```{code} python
   @job("dependency1", "dependency2", desc="Can't think of a good description", default=True)
   def my_jobname():
        # ...
```

Dependencies are specified in a list, and all arguments to the `@job` decorator are optional.

## pogfile Features

pogfiles are python files with a few python imports set.

```{literalinclude} ../../pogmake.py
    :start-after: pogfile shared imports
    :end-before: /pogfile shared imports
    :language: python
```

Additionally there are a few library functions from pogmake that get imported as well.

```{literalinclude} ../../importer.py
    :start-after: pogfile extra symbols
    :end-before: /pogfile extra symbols
    :language: python
```
By default all pogfiles in inferior pathsto the root are searched for. 

Use `exclude_paths` to skip them.

`include_paths` will also bypass this. And allow you to pull in pogfiles of any any name.

```{literalinclude} ../../tests/pogfile.py
    :start-after: include exclude
    :end-before: /include exclude
    :language: python
```
