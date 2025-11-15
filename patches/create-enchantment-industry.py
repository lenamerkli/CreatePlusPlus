import os
import pathlib
import subprocess
import random
import re

URL = 'https://github.com/DragonsPlusMinecraft/CreateEnchantmentIndustry-Fabric.git'
COMMIT = '0d8640b4f915d75cb420fcbd4e08cf89737a349c'
BRANCH = '1.20.1/0.5.1-dev'
TEMP = f"/tmp/create-enchantment-industry-fabric/{os.getpid()}{random.randint(10 ** 6, 10 ** 7)}"
PATCH_VERSION = '1.0'


if __name__ == '__main__':
    if os.name != 'posix':
        raise RuntimeError('This script only works on Linux')

    print(f'Patching Create Enchantment Industry with version {PATCH_VERSION} in `{TEMP}`')

    if os.path.exists(TEMP):
        raise RuntimeError(f'`{TEMP}` already exists, aborting')

    # Create directory
    pathlib.Path(TEMP).mkdir(parents=True, exist_ok=True)

    # Run git clone
    subprocess.run(['git', 'clone', '--branch', BRANCH, '--single-branch', URL], cwd=TEMP, check=True, stdout=None)

    # Run git checkout to specific commit
    subprocess.run(['git', 'checkout', COMMIT], cwd=os.path.join(TEMP, 'CreateEnchantmentIndustry-Fabric'), check=True, stdout=None)

    # `fabric.mod.json`
    with open(os.path.join(TEMP, 'CreateEnchantmentIndustry-Fabric/src/main/resources/fabric.mod.json'), 'r+') as file:
        content = file.read()
        # add author
        content = re.sub(r'"authors": \[', '"authors": [\n    "LenaMerkli",', content)
        # write
        file.seek(0)
        file.write(content)
        file.truncate()

    with open(os.path.join(TEMP, 'CreateEnchantmentIndustry-Fabric/src/main/java/plus/dragons/createenchantmentindustry/foundation/config/CeiServerConfig.java'), 'r+') as file:
        content = file.read()
        # change copier tank capacity (flexible for upstream changes)
        content = re.sub(r'public final ConfigInt copierTankCapacity = i\([^,\n]*,', 'public final ConfigInt copierTankCapacity = i(16000,', content)
        # write
        file.seek(0)
        file.write(content)
        file.truncate()

    # `build.gradle`
    with open(os.path.join(TEMP, 'CreateEnchantmentIndustry-Fabric/build.gradle'), 'r+') as file:
        content = file.read()
        # replace maven repository
        content = content.replace('maven.tterrag.com', 'modmaven.dev')
        # write
        file.seek(0)
        file.write(content)
        file.truncate()

    # build
    subprocess.run(['./gradlew', 'build', '--refresh-dependencies'], cwd=os.path.join(TEMP, 'CreateEnchantmentIndustry-Fabric'), check=True, stdout=None)

    # make dir
    pathlib.Path('~/Desktop/create-enchantment-industry-fabric/').expanduser().mkdir(parents=True, exist_ok=True)

    # copy jar
    file_list = os.listdir(os.path.join(TEMP, 'CreateEnchantmentIndustry-Fabric/build/libs/'))
    file = None
    for f in file_list:
        if f.endswith('.jar') and 'source' not in f:
            file = f
    if file is None:
        raise RuntimeError('No jar file found')
    subprocess.run(['cp', os.path.join(TEMP, 'CreateEnchantmentIndustry-Fabric/build/libs/', file), os.path.join(pathlib.Path('~/Desktop/create-enchantment-industry-fabric/').expanduser(), file)], check=True, stdout=None)
