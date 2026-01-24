import os
import pathlib
import subprocess
import random
import re

URL = 'https://github.com/CaffeineMC/sodium.git'
COMMIT = '1bcd392f241a44bc454582dad97e7f2a6c1ad01b'
BRANCH = '1.20.1/stable-0.5'
TEMP = f"/tmp/sodium/{os.getpid()}{random.randint(10 ** 6, 10 ** 7)}"
VERSION = 'sodium-fabric-0.5.13+mc1.20.1+createplusplus1.0'


if __name__ == '__main__':
    if os.name != 'posix':
        raise RuntimeError('This script only works on Linux')

    print(f'Patching Create with version {VERSION} in `{TEMP}`')

    if os.path.exists(TEMP):
        raise RuntimeError(f'`{TEMP}` already exists, aborting')

    # Create directory
    pathlib.Path(TEMP).mkdir(parents=True, exist_ok=True)

    # Run git clone
    subprocess.run(['git', 'clone', '--branch', BRANCH, '--single-branch', URL], cwd=TEMP, check=True, stdout=None)

    # Run git checkout
    subprocess.run(['git', 'checkout', COMMIT], cwd=os.path.join(TEMP, 'sodium'), check=True, stdout=None)

    with open(os.path.join(TEMP, 'sodium/src/main/java/me/jellysquid/mods/sodium/client/world/WorldSlice.java'), 'r+') as file:
        content = file.read()
        # change chances
        content = content.replace('    private final ClientWorld world;', '    public final ClientWorld world;')
        # write
        file.seek(0)
        file.write(content)
        file.truncate()

    # build
    subprocess.run(['./gradlew', 'build'], cwd=os.path.join(TEMP, 'sodium'), check=True, stdout=None, env={'JAVA_HOME': '/home/lena/.jdks/temurin-17.0.13'})

    # make dir
    pathlib.Path('~/Desktop/create_plusplus/').expanduser().mkdir(parents=True, exist_ok=True)

    # copy jar
    file_list = os.listdir(os.path.join(TEMP, 'sodium/build/libs/'))
    file = None
    for f in file_list:
        if f.endswith('.jar') and 'source' not in f:
            file = f
    if file is None:
        raise RuntimeError('No jar file found')
    subprocess.run(['cp', os.path.join(TEMP, 'sodium/build/libs/', file), os.path.join(pathlib.Path('~/Desktop/create_plusplus/').expanduser(), file)], check=True, stdout=None)

