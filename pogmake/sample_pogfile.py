# do not look for pogfiles in this directory
# exclude_paths = ["dont_include"]  

# these files/directories shall be imported, even if they're out of path or if they're 
# include_paths = ["test_simple.py", "dont_include/test_anyway/"] 


@job(desc="Hello World job, this is the toplevel default target")
def all():
    print("Hello friend! from python")
    env.system("echo hello world from the system shell")
    env.run("echo", "hello!")