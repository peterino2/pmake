# Design Information

The design of the pogfile system is intended to do one thing really well. 

"Register jobs and run them as flexibly as possbile."

The main story it's meant to fill is.

"If I write a console command once, I shouldn't have to write it again."

## Runtime description

When `pog` runs it will accept either a path to a folder or file. And read it
as a python module.

- It will inject various python objects into that module's namespace (such as
  `job` and other pog system controls).
- It will load submodules according to the [submodule rules](Submodule Rules).
- functions decorated with @job will be added to the global jobs manager and 
appear as runnable targets through pog

## Submodule Rules

The first `pogfile` that is read in shall be the the main pogfile for the
project.

```{note}
Note this does not have to be a `pogfile` it could be named whatever you want
but then the path argument will have to specify that target
```

If the pogfile sets the variable `autoindex = true` then all inferior folders
shall be walked and any `pogfile.py` shall automatically be added to the jobs
description. 
