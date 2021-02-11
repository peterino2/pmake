
@job(desc="Hello World job, this is the toplevel default target")
def all():
    print("Hello friend! from python")
    env.system("echo hello world from the system shell")
    env.run('git', 'status')