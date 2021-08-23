import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrapy-agentfive-middleware",
    version="0.0.1",
    license="MIT",
    description="Scrapy downloader middleware to interact with agentfive API",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="agentfive",
    author_email="service@agentfive.cn",
    url="https://github.com/agentfivecn/scrapy-agentfive-middleware",
    packages=["agentfive_middleware"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: Scrapy",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.5",
    install_requires=["scrapy>=1.6.0"],
)
