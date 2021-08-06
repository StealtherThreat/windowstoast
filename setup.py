import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="windowstoast",
    version="0.0.3",
    author="Tushar Goyal",
    author_email="StealtherThreat@outlook.com",
    description="Toast notifications for Windows 10",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StealtherThreat/windowstoast",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    python_requires='>=3.6',
)
