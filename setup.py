from setuptools import setup, find_packages

setup(
    name='SOP',  # Nombre del paquete
    version='0.1',  # Versión del paquete
    packages=find_packages(),  # Encuentra automáticamente los paquetes del proyecto
    install_requires=[  # Lista de dependencias necesarias para el paquete
        'numpy',
        'matplotlib'
    ],
    author='Tu Nombre',  # Tu nombre
    author_email='tu@email.com',  # Tu correo electrónico
    description='Una descripción corta de tu paquete',  # Descripción breve del paquete
    url='https://github.com/pssngalarce/SOP.git',  # URL del repositorio del proyecto
)
