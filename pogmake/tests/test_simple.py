@job("job1", desc="Job 2 depends on job 1")
def job2():
    print("job2")

@job("job4")
def job4():
    print("job4")

@job(desc="Some job that stands alone")
def job3():
    print("job3")

@job(desc="job1's generator function")
def job1_gen():
    print("job1_gen")

@job("job1_gen", desc="job1's main build")
def job1():
    print("job1")

@job("job1", desc="a test of job1", default=False)
def job1_test():
    print("job1's test")
