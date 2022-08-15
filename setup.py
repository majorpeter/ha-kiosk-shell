from setuptools import setup, find_packages

with open('requirements.txt') as requirement_file:
    requirements = requirement_file.read().split()

setup(
    name='ha_kiosk_shell',
    description='Windows shell replacement for a Home Automation Kiosk application in Python',
    version='1.0.0',
    author='Major Peter',
    author_email='majorpeter29@gmail.com',
    install_requires=requirements,
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    python_requires=">=3.10, <4",
    entry_points={
        'console_scripts': ['ha_kiosk_shell = ha_kiosk_shell:main']
    }
)
