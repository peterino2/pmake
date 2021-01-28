.. Embersong documentation master file, created by
   sphinx-quickstart on Sat Jan 16 10:59:11 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pogmake! - Peterino's Python Pog as heck make tool 
==================================================

=================
Executive summary
=================

I got really tired of writing makefiles and having it all work in a cross platform manner. 

So I'm writing a python tool that abuses the crap out of python meta-attributes and importlib to basically let me write deterministic build scripts in python that would work in all the CI systems I have to support at my day job.

===============
Quickstart
===============

Pmake files are python files with access to a specific environment.
To get started

.. code:: python

   # pogfile.py
   @job(desc="Configure and build with cmake")
   def my_jobname():
       os.makedirs("build", exist_ok=True)
       subprocess.run(["cmake", orig_dir, "-GNinja"], cwd="build")

Becomes

.. code:: text

   ======================================================================
   There is 1 job registered: (* means part of the default)
      * my_jobname - Configure and build with cmake
   ======================================================================
   

Even the automation and CI for this repo is done with pogmake.
To get a glimpse of that, run ``python .`` to see all the jobs are available in pogmake itself.

===============
Usage
===============

.. literalinclude:: _spec/usage_print.txt
   :language: text

Btw the usage file seen above is auto-generated based on whatever the output of `pogmake --help` is here's an example of the code to do that.

.. literalinclude:: ../pogfile.py
   :start-after: usage_print_example
   :end-before: /usage_print_example
   :language: python


Further Reading
==================

.. toctree::
   :maxdepth: 2

   reference/cheatsheet.md



.. * :ref:`genindex`
.. * :ref:`search`
