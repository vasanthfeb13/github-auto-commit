from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="github-auto-commit",
    version="1.0.1",  # Match with our latest tag
    author="Vasanth Adithya",
    author_email="vasanthfeb13@gmail.com",
    description="A powerful command-line tool for automating GitHub contributions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vasanthfeb13/github-auto-commit",
    project_urls={
        "Bug Tracker": "https://github.com/vasanthfeb13/github-auto-commit/issues",
        "Documentation": "https://github.com/vasanthfeb13/github-auto-commit#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "rich>=10.0.0",
        "requests>=2.25.0",
        "python-dotenv>=0.19.0",
        "questionary>=1.10.0",
    ],
    entry_points={
        "console_scripts": [
            "github-auto-commit=github_auto_commit.cli:main",
        ],
    },
)
