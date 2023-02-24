from setuptools import find_packages, setup

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
    name='crawler-helper',  # 应用名
    packages=find_packages(),
    version='0.1.0',  # 版本号
    description='Help you to build web crawlers',
    url='https://github.com/taoohong/crawler-helper',
    author='TaoHong',
    license='MIT',
    install_requires=[
        "requests==2.28.1",
        "retrying==1.3.4",
        "selenium==4.3.0",
        "XlsxWriter==3.0.3"
        "APScheduler==3.9.1"
    ],  # 依赖列表
    
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    # test
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.4'],
    test_suite='tests',
)
