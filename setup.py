from setuptools import setup


setup(
    name='pyginator',
    version='0.1.0',
    description='pyginator - static web site generator',
    author='Alexander Finn',
    author_email='finnam@gmail.com',
    url='https://github.com/alexanderfinn/pyginator',
    packages=['pyginator',],
    install_requires=["Jinja2", "boto3"],
)