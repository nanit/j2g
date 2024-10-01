import setuptools
setuptools.setup(
    name='j2g',
    version='1.0',
    author='quatrix',
    description='converts pydantic to glue schema to use with terraform',
    packages=['j2g'],
    entry_points = {
        'console_scripts': ['j2g=j2g.cli:cli'],
    },
    install_requires=[
        'setuptools',
        'jsonref==0.2',
        'pydantic==1.10.13',
        'typing_extensions==4.2.0',
    ],
    python_requires='>=3.8'
)
