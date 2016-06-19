from setuptools import setup


setup(
    name='pyginator',
    version='0.3.0',
    description='pyginator - static web site generator',
    author='Alexander Finn',
    author_email='finnam@gmail.com',
    url='https://github.com/alexanderfinn/pyginator',
    packages=['pyginator',],
    install_requires=["Jinja2", "boto3", "markdown"],
    entry_points = {
        'console_scripts': ['pyginator=pyginator.pyginator:command_line'],
    },
)