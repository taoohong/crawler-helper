from setuptools import find_packages, setup

setup(
    name='crawler-helper',  # 应用名
    packages=find_packages(),
    version='0.1.0',  # 版本号
    description='Help you to build web crawlers',
    author='TaoHong',
    license='MIT',
    install_requires=[
            "requests==2.28.1",
            "retrying==1.3.4",
            "selenium==4.3.0",
            "XlsxWriter==3.0.3"
    ],  # 依赖列表
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.4'],
    test_suite='tests',
)
