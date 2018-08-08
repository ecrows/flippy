from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name = 'flippy',
    version = '0.1.2',
    description = 'Build videos from image directories',
    long_description = long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Video',
    ],
    keywords = 'opencv video flipbook overlay python3 timelapse lapse flip flipy',
    url = 'https://github.com/ecrows/flippy',
    author = 'ecrows',
    license = 'MIT',
    packages = ['flippy'],
    install_requires=[
        'numpy',
        'opencv-python',
    ],
    entry_points = {
        'console_scripts': [
            'flippy = flippy.__main__:main'
        ]
    })
