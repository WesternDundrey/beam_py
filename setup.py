# setup.py

from setuptools import setup, find_packages

setup(
    name='beam_py', 
    version='0.1.0',  
    description='A simple beam stress visualization library for young learners',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='westerndundrey',
    author_email='hijackedpuffin@gmail.com',
    url='https://github.com/WesternDundrey/beam_py',  
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'plotly',
        'dash',
        'dash-bootstrap-components',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',  
        'Intended Audience :: Education',
        'Topic :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'beam-py-app=beam_py.app:main',  
        ],
    },
    include_package_data=True,  
    python_requires='>=3.6',  
)
