from setuptools import setup, find_packages

setup(
    name='chargrid',
    version='0.0.4',
    description='HackNet-style grid-based game engine framework.',
    author='James Evans',
    author_email='joesaysahoy@gmail.com',
    url='https://github.com/primal-coder/chargrid',
    packages=find_packages(),
    install_requires=[
        'gridengine_framework>=0.9.9', 
        'CharActor>=1.0.5', 
        'CharMonster>=0.1.5', 
        'CharObj>=0.2.1',
        'CharTask>=0.0.6', 
        'dicepy>=0.4', 
        'entyty>=0.0.54'],
    keywords='gridengine_framework CharActor grid character rpg game engine framework chargrid cell grid-based cell-based dnd d&d dungeons and dragons dungeon dragons'    
)