from setuptools import setup, find_packages

setup(name='Gnip-Analysis-Tools',
        packages=find_packages(),
        version='0.1',
        license='MIT',
        author='Jeff Kolb',
        author_email='jeffakolb@gmail.com',
        description='Configuration tools for Gnip-Analysis-Pipeline',  
        extras_require = {'nltk' : 'nltk'},
        url='https://github.com/tw-ddis/Gnip-Analysis-Tools',
        )
