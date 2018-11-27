import codecs

from setuptools import setup

try:
    f = codecs.open('requirements.txt', encoding='utf-8')
    requirements = f.read().splitlines()
    f.close()
except:
    requirements = []

setup(
    name='jwt-validation',
    version='0.1',
    description='JWT validation tool',
    url='http://github.com/Lululemon/jwt-validation-tool',
    author='Thiago Papageorgiou',
    author_email='tpapageorgiou@lululemon.com',
    license='UNLICENSED',
    packages=['jwt_validation'],
    entry_points = {
        'console_scripts': ['jwt-validation=jwt_validation.jwt_validation:main'],
    },
    install_requires=requirements,
)
