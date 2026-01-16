# from setuptools import find_packages, setup
# import os  
# from glob import glob  

# package_name = 'touch_mapper'

# setup(
#     name=package_name,
#     version='0.0.0',
#     packages=find_packages(exclude=['test']),
#     data_files=[
#         ('share/ament_index/resource_index/packages',
#             ['resource/' + package_name]),
#         ('share/' + package_name, ['package.xml']),
#         (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
#     ],
#     install_requires=['setuptools'],
#     zip_safe=True,
#     maintainer='beginner',
#     maintainer_email='beginner@todo.todo',
#     description='TODO: Package description',
#     license='TODO: License declaration',
#     extras_require={
#         'test': [
#             'pytest',
#         ],
#     },
#     entry_points={
#     'console_scripts': [
#         'trajectory_projector = touch_mapper.trajectory_projector:main',
#         ],
#     },
# )
from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'touch_mapper'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),  # 自动发现 touch_mapper/ 目录（需有 __init__.py）
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your@email.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'trajectory_projector = touch_mapper.trajectory_projector:main',
        ],
    },
)