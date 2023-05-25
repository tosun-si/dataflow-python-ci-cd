from setuptools import find_packages, setup

setup(
    name="team_league_app",
    version="0.0.1",
    install_requires=[
        'dacite==1.6.0',
        'toolz==0.11.1',
        'pampy==0.3.0'
    ],
    packages=find_packages(),
)
