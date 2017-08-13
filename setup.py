from setuptools import setup

setup(name='namegenerator',
      version='0.1',
      description='This one generates names',
      author='Liffon',
      author_email='liffon@gmail.com',
      url='https://github.com/Liffon/name-generator',
      install_requires=['numpy'],
      packages=['namegenerator'],
      package_data={'': ['dist.female.first.txt',
                         'dist.male.first.txt',
                         'swedish-female-firstnames.csv',
                         'swedish-male-firstnames.csv']},
      scripts=['bin/namegenerator'],
     )
