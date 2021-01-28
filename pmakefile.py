# usage_print_example
docs_spec_folder = path.abspath(path.join("docs_src/_spec"))
usage_print_file = path.join(docs_spec_folder, "usage_print.txt")

@job(desc="Prints the 'usage' to the temporary directory under ")
def usage_print():
    os.makedirs("docs_src/_spec", exist_ok=True)
    output = sp.check_output([sys.executable, ".", "--help"])
    with open(usage_print_file, "w") as f:
        f.write(output.decode())
# /usage_print_example

    

@job("usage_print", desc="Builds the documentation for pmake")
def docs():
    os.makedirs("build-html", exist_ok=True)
    sp.run(['sphinx-build', 'docs_src', 'build-html'], check=True)

@job(desc="Runs the tests for pmake", default=False)
def tests():
    cmd = [sys.executable, "-m", "pytest", verbosity]
    if cli_args.verbosity == "DEBUG":
        cmd.append("-vvv")
    sp.run(cmd, check=True)

