
exclude_paths = ["tests"]    # do not look for pogfiles in this directory

path = os.path

docs_spec_folder = path.abspath(path.join("docs_src/_spec"))
usage_print_file = path.join(docs_spec_folder, "usage_print.txt")

# usage_print_example
@job(desc="Prints the 'usage' to the temporary directory under ")
def usage_print():
    os.makedirs("docs_src/_spec", exist_ok=True)
    output = subprocess.check_output([sys.executable, ".", "--help"])
    with open(usage_print_file, "w") as f:
        f.write(output.decode())

@job("usage_print", desc="Builds the documentation for pogmake")
def docs():
    os.makedirs("build-html", exist_ok=True)
    subprocess.run(['sphinx-build', 'docs_src', 'build-html'], check=True)
# /usage_print_example

@job(desc="Runs the tests for pogmake", default=True)
def tests():
    subprocess.run(['python', '..' , '--list'], check=True, cwd='tests')

