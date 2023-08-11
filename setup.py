from setuptools import setup

setup(
    name='mantle',
    url='https://github.com/phanrahan/mantle',
    license='MIT',
    author='Pat Hanrahan',
    maintainer='Pat Hanrahan',
    maintainer_email='hanrahan@cs.stanford.edu',
    description='The magma standard library',
    packages=[
        "mantle",
        "mantle.lattice",
        "mantle.lattice.mantle40",
        "mantle.lattice.ice40",
        "mantle.verilog"
    ],

    install_requires=[
        "six"
    ],
    python_requires='>=3.6'
)
