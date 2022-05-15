from setuptools import setup, find_packages

setup(
    # 以下为必需参数
    name='fAES',  # 模块名
    version='1.0.0',  # 当前版本
    description='Use AES to encrypt & decrypt your files',  # 简短描述
    # py_modules=[""], # 单文件模块写法
    ckages=find_packages(),

    # 以下均为可选参数
    url='https://github.com/FHYQ-DHY/fAES', # 主页链接
    author='FHYQ_DHY', # 作者名
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',    #对python的最低版本要求

)