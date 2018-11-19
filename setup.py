from distutils.core import setup

with open('README') as f:
    long_description = f.read()

setup(
    name='FunctionalCache',
    description='SQLite function cache',
    version='0.1',
    packages=['functional_cache', ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/thomas9911/FunctionalCache',
    author='thomas9911',
    author_email='thomastimmer11@hotmail.com'
)
