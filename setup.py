from setuptools import setup, find_packages

setup(
    name='chargrid',
    version='0.0.2',
    description='An implementation of gridengine_framework and the CharActor that combines the two',
    author='James Evans',
    author_email='joesaysahoy@gmail.com',
    url='https://github.com/primal-coder/chargrid',
    packages=find_packages(),
    install_requires=['gridengine_framework', 'CharActor'],
    keywords='gridengine_framework CharActor grid character rpg game engine framework chargrid cell grid-based cell-based dnd d&d dungeons and dragons dungeon dragons'    
)