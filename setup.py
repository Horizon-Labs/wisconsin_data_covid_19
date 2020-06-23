import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Horizon Labs", # Replace with your own username
    version="0.0.1",
    author="T.Rose",
    author_email="roset21@muhs.edu",
    description="tools for analyzing data regarding COVID-19 in Wisconsin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Horizon-Labs/wisconsin_data_covid_19.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)
