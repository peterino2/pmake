
# include exclude
exclude_paths = ["dont_test"]   
include_paths = ["test_simple.py", "dont_test/test_anyway/"]
# /include exclude

@job("self_depends")
def self_depends(): 
    pass

@job()
def root():
    pass

@job("self_depends", "root")
def root2():
    pass


@job("x1", "root")
def x3():
    pass

@job("x3", "root")
def x4():
    pass

@job("x4", "root")
def x5():
    pass


@job("3rdparty", desc="I depend on things that don't exist") 
def sublib1(): pass

@job(desc="WHOO I HAVE A DESCRIPTION") 
def sublib2(): pass

@job() 
def sublib3(): pass

@job() 
def sublib4(): pass

@job() 
def sublib5(): pass

@job(
    "sublib1",
    "sublib2",
    "sublib3",
    "sublib4",
    "sublib5",
)
def lib1(): pass


@job("x5")
def lib2(): pass

@job("lib1", "lib2", "job2")
def top(): pass





