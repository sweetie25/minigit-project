from setuptools import setup, find_packages

setup(
    name="minigit",
    version="0.1.0",
    description="MiniGit: A Custom Version Control System",
    author="Your Name",
    author_email="you@example.com",
    url="https://github.com/yourusername/minigit",  # update as appropriate
    packages=find_packages(where=".", exclude=["tests*", "docs*"]),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        # no external dependencies—only standard library
    ],
    entry_points={
        "console_scripts": [
            "minigit = minigit.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
