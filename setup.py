from setuptools import setup
setup(
    name = 'flippy',
    version = '0.1.0',
    packages = ['flippy'],
    entry_points = {
        'console_scripts': [
            'flippy = flippy.__main__:main'
        ]
    }
    install_requires=[
        'numpy',
        'opencv-python'
    ])