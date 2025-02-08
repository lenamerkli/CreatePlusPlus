import os
import pathlib
import subprocess
import random
import re

URL = 'https://github.com/Fabricators-of-Create/Create.git'
TEMP = f"/tmp/create/{os.getpid()}{random.randint(10 ** 6, 10 ** 7)}"
PATCH_VERSION = '8.0'


if __name__ == '__main__':
    if os.name != 'posix':
        raise RuntimeError('This script only works on Linux')

    print(f'Patching Create with version {PATCH_VERSION} in `{TEMP}`')

    if os.path.exists(TEMP):
        raise RuntimeError(f'`{TEMP}` already exists, aborting')

    # Create directory
    pathlib.Path(TEMP).mkdir(parents=True, exist_ok=True)

    # Run git clone
    subprocess.run(['git', 'clone', URL], cwd=TEMP, check=True, stdout=None)

    # `gradle.properties`
    with open(os.path.join(TEMP, 'Create/gradle.properties'), 'r+') as file:
        content = file.read()
        # change recipe viewer to `Roughly Enough Items`
        content = re.sub(r'recipe_viewer = [.]{3}', r'recipe_viewer = rei', content)
        # change version

        original_version = re.search(r'mod_version = ([^,\n]*)', content).group(1)
        content = re.sub(r'mod_version = [^,\n]*', f'mod_version = {original_version.strip()}-create_plusplus{PATCH_VERSION}', content)
        # write
        file.seek(0)
        file.write(content)
        file.truncate()

    # `rose_quartz.json`
    with open(os.path.join(TEMP, 'Create/src/generated/resources/data/create/recipes/crafting/materials/rose_quartz.json'), 'r+') as file:
        content = file.read()
        # remove half of the required redstone dust
        content = content.replace('    {\n        "tag": "c:dusts/redstone"\n    },\n', '', 4)
        # write
        file.seek(0)
        file.write(content)
        file.truncate()

    # `tuff.json`
    with open(os.path.join(TEMP, 'Create/src/generated/resources/data/create/recipes/crushing/tuff.json'), 'r+') as file:
        content = file.read()
        # change chances
        content = content.replace('"chance": 0.25', '"chance": 0.3')
        content = content.replace('"chance": 0.1', '"chance": 0.2')
        # write
        file.seek(0)
        file.write(content)
        file.truncate()

    # `ContraptionData.java`
    with open(os.path.join(TEMP, 'Create/src/main/java/com/simibubi/create/content/contraptions/ContraptionData.java'), 'r+') as file:
        content = file.read()
        # change default limit
        content = re.sub(r'public static final int DEFAULT_LIMIT = [^;\n]*;', 'public static final int DEFAULT_LIMIT = 20_000_000;', content)
        # write
        file.seek(0)
        file.write(content)
        file.truncate()

    # `CClient.java`
    with open(os.path.join(TEMP, 'Create/src/main/java/com/simibubi/create/infrastructure/config/CClient.java'), 'r+') as file:
        content = file.read()
        # change zoom multiplier

        content = re.sub(r'public final ConfigFloat mountedZoomMultiplier = f\([^,\n]*,', 'public final ConfigFloat mountedZoomMultiplier = f(2,', content)
        # automatically show track graph
        content = content.replace('public final ConfigBool showTrackGraphOnF3 = b(false,', 'public final ConfigBool showTrackGraphOnF3 = b(true,')
        # write
        file.seek(0)
        file.write(content)
        file.truncate()

    # `CFluids.java`
    with open(os.path.join(TEMP, 'Create/src/main/java/com/simibubi/create/infrastructure/config/CFluids.java'), 'r+') as file:
        content = file.read()
        # change block threshold
        content = re.sub(r'public final ConfigInt hosePulleyBlockThreshold = i\([^,\n]*,', 'public final ConfigInt hosePulleyBlockThreshold = i(4096,', content)
        # automatically fill infinite
        content = content.replace('public final ConfigBool fillInfinite = b(false,', 'public final ConfigBool fillInfinite = b(true,')
        # write
        file.seek(0)
        file.write(content)
        file.truncate()

    # `CKinetics.java`
    with open(os.path.join(TEMP, 'Create/src/main/java/com/simibubi/create/infrastructure/config/CKinetics.java'), 'r+') as file:
        content = file.read()
        # change max blocks moved
        content = re.sub(r'public final ConfigInt maxBlocksMoved = i\([^,\n]*,', 'public final ConfigInt maxBlocksMoved = i(65535,', content)
        # write
        file.seek(0)
        file.write(content)
        file.truncate()

    # `CLogistics.java`
    with open(os.path.join(TEMP, 'Create/src/main/java/com/simibubi/create/infrastructure/config/CLogistics.java'), 'r+') as file:
        content = file.read()
        # change default extraction timer
        content = re.sub(r'public final ConfigInt defaultExtractionTimer = i\([^,\n]*,', 'public final ConfigInt defaultExtractionTimer = i(2,', content)
        # change displaylink range
        content = re.sub(r'public final ConfigInt displayLinkRange = i\([^,\n]*,', 'public final ConfigInt displayLinkRange = i(256,', content)
        # change brass tunnel timer
        content = re.sub(r'public final ConfigInt brassTunnelTimer = i\([^,\n]*,', 'public final ConfigInt brassTunnelTimer = i(2,', content)
        # write
        file.seek(0)
        file.write(content)
        file.truncate()

    # `CSchematics.java`
    with open(os.path.join(TEMP, 'Create/src/main/java/com/simibubi/create/infrastructure/config/CSchematics.java'), 'r+') as file:
        content = file.read()
        # change max schematics
        content = re.sub(r'public final ConfigInt maxSchematics = i\([^,\n]*,', 'public final ConfigInt maxSchematics = i(24,', content)
        # change max total schematic size
        content = re.sub(r'public final ConfigInt maxTotalSchematicSize = i\([^,\n]*,', 'public final ConfigInt maxTotalSchematicSize = i(2048,', content)
        # change max schematic packet size
        content = re.sub(r'public final ConfigInt maxSchematicPacketSize = \n? i\([^,\n]*,', 'public final ConfigInt maxSchematicPacketSize = i(1024,', content)
        # change schematicannon delay
        content = re.sub(r'public final ConfigInt schematicannonDelay = i\([^,\n]*,', 'public final ConfigInt schematicannonDelay = i(1,', content)
        # write
        file.seek(0)
        file.write(content)
        file.truncate()

    # `CTrains.java`
    with open(os.path.join(TEMP, 'Create/src/main/java/com/simibubi/create/infrastructure/config/CTrains.java'), 'r+') as file:
        content = file.read()
        # change max track placement length
        content = re.sub(r'public final ConfigInt maxTrackPlacementLength = i\([^,\n]*, [^,\n]*, [^,\n]*,', 'public final ConfigInt maxTrackPlacementLength = i(128, 16, 256,', content)
        # change max assembly length
        content = re.sub(r'public final ConfigInt maxAssemblyLength = i\([^,\n]*,', 'public final ConfigInt maxAssemblyLength = i(270,', content)
        # change max bogey count
        content = re.sub(r'public final ConfigInt maxBogeyCount = i\([^,\n]*,', 'public final ConfigInt maxBogeyCount = i(48,', content)
        # change manual train speed modifier
        content = re.sub(r'public final ConfigFloat manualTrainSpeedModifier = f\([^,\n]*,', 'public final ConfigFloat manualTrainSpeedModifier = f(.86f,', content)
        # change train top speed
        content = re.sub(r'public final ConfigInt trainTopSpeed = i\([^,\n]*,', 'public final ConfigInt trainTopSpeed = i(24,', content)
        # change train turning top speed
        content = re.sub(r'public final ConfigInt trainTurningTopSpeed = i\([^,\n]*,', 'public final ConfigInt trainTurningTopSpeed = i(12,', content)
        # change train acceleration
        content = re.sub(r'public final ConfigFloat trainAcceleration = i\([^,\n]*,', 'public final ConfigFloat trainAcceleration = i(2.5f,', content)
        # change powered train top speed
        content = re.sub(r'public final ConfigInt poweredTrainTopSpeed = i\([^,\n]*,', 'public final ConfigInt poweredTrainTopSpeed = i(36,', content)
        # change powered train turning top speed
        content = re.sub(r'public final ConfigInt poweredTrainTurningTopSpeed = i\([^,\n]*,', 'public final ConfigInt poweredTrainTurningTopSpeed = i(20,', content)
        # change powered train acceleration
        content = re.sub(r'public final ConfigFloat poweredTrainAcceleration = i\([^,\n]*,', 'public final ConfigFloat poweredTrainAcceleration = i(3f,', content)
        # write
        file.seek(0)
        file.write(content)
        file.truncate()

    # `fabric.mod.json`
    with open(os.path.join(TEMP, 'Create/src/main/resources/fabric.mod.json'), 'r+') as file:
        content = file.read()
        # add author
        content = re.sub(r'"authors": \[', '"authors": [\n    "Lenamerkli",', content)
        # replace contacts
        content = re.sub(r'"issues": "[^\n]*",', '"issues": "https://github.com/Lenamerkli/Create/issues",', content)
        content = re.sub(r'"sources": "[^\n]*",', '"sources": "https://github.com/Lenamerkli/Create",', content)
        # write
        file.seek(0)
        file.write(content)
        file.truncate()

    pathlib.Path(os.path.join(TEMP, 'Create/src/main/resources/data/create/recipes/lenamerkli')).mkdir(parents=True, exist_ok=True)

    # add `asurine_compacting.json`
    with open(os.path.join(TEMP, 'Create/src/main/resources/data/create/recipes/lenamerkli/asurine_compacting.json'), 'w') as file:
        file.write('{\n  "type": "create:compacting",\n  "ingredients": [\n    {\n      "item": "minecraft:tuff"\n    },\n    {\n      "item": "minecraft:andesite"\n    },\n    {\n      "fluid": "minecraft:lava",\n      "nbt": {},\n      "amount": 12000\n    }\n  ],\n  "results": [\n    {\n      "item": "create:asurine",\n      "count": 2\n    }\n  ]\n}')

    # add `calcite_mixing.json`
    with open(os.path.join(TEMP, 'Create/src/main/resources/data/create/recipes/lenamerkli/calcite_mixing.json'), 'w') as file:
        file.write('{\n  "type": "create:mixing",\n  "ingredients": [\n    {\n      "item": "minecraft:diorite"\n    },\n    {\n      "item": "minecraft:quartz"\n    },\n    {\n      "fluid": "minecraft:lava",\n      "nbt": {},\n      "amount": 8000\n    }\n  ],\n  "results": [\n    {\n      "item": "minecraft:calcite"\n    }\n  ]\n}')

    # add `cobbled_deepslate_compacting.json`
    with open(os.path.join(TEMP, 'Create/src/main/resources/data/create/recipes/lenamerkli/cobbled_deepslate_compacting.json'), 'w') as file:
        file.write('{\n  "type": "create:compacting",\n  "ingredients": [\n    {\n      "item": "minecraft:cobblestone"\n    },\n    {\n      "fluid": "minecraft:lava",\n      "nbt": {},\n      "amount": 22000\n    }\n  ],\n  "results": [\n    {\n      "item": "minecraft:cobbled_deepslate",\n      "count": 1\n    }\n  ]\n}')

    # add `crimsite_compacting.json`
    with open(os.path.join(TEMP, 'Create/src/main/resources/data/create/recipes/lenamerkli/crimsite_compacting.json'), 'w') as file:
        file.write('{\n  "type": "create:compacting",\n  "ingredients": [\n    {\n      "item": "minecraft:tuff"\n    },\n    {\n      "item": "minecraft:diorite"\n    },\n    {\n      "fluid": "minecraft:lava",\n      "nbt": {},\n      "amount": 15000\n    }\n  ],\n  "results": [\n    {\n      "item": "create:crimsite",\n      "count": 2\n    }\n  ]\n}')

    # add `diorite_mixing.json`
    with open(os.path.join(TEMP, 'Create/src/main/resources/data/create/recipes/lenamerkli/diorite_mixing.json'), 'w') as file:
        file.write('{\n  "type": "create:mixing",\n  "ingredients": [\n    {\n      "item": "minecraft:cobblestone"\n    },\n    {\n      "item": "minecraft:quartz"\n    }\n  ],\n  "results": [\n    {\n      "item": "minecraft:diorite"\n    }\n  ]\n}')

    # add `glowstone_dust_crushing.json`
    with open(os.path.join(TEMP, 'Create/src/main/resources/data/create/recipes/lenamerkli/glowstone_dust_crushing.json'), 'w') as file:
        file.write('{\n  "type": "create:crushing",\n  "ingredients": [\n    {\n      "item": "create:ochrum"\n    }\n  ],\n  "processingTime": 250,\n  "results": [\n    {\n      "chance": 0.25,\n      "item": "minecraft:glowstone_dust"\n    },\n    {\n      "chance": 0.5,\n      "item": "minecraft:tuff"\n    },\n    {\n      "chance": 0.5,\n      "item": "minecraft:granite"\n    }\n  ]\n}')

    # add `industrial_iron_block_stonecutting.json`
    with open(os.path.join(TEMP, 'Create/src/main/resources/data/create/recipes/lenamerkli/industrial_iron_block_stonecutting.json'), 'w') as file:
        file.write('{\n  "type": "minecraft:stonecutting",\n  "count": 1,\n  "ingredient": {\n    "item": "minecraft:iron_block"\n  },\n  "result": "create:industrial_iron_block"\n}')

    # add `limestone_mixing.json`
    with open(os.path.join(TEMP, 'Create/src/main/resources/data/create/recipes/lenamerkli/limestone_mixing.json'), 'w') as file:
        file.write('{\n  "type": "create:mixing",\n  "ingredients": [\n    {\n      "item": "minecraft:cobblestone"\n    },\n    {\n      "item": "minecraft:quartz"\n    },\n    {\n      "amount": 8000,\n      "fluid": "minecraft:lava",\n      "nbt": {}\n    }\n  ],\n  "results": [\n    {\n      "count": 1,\n      "item": "create:limestone"\n    }\n  ]\n}')

    # add `ochrum_compacting.json`
    with open(os.path.join(TEMP, 'Create/src/main/resources/data/create/recipes/lenamerkli/ochrum_compacting.json'), 'w') as file:
        file.write('{\n  "type": "create:compacting",\n  "ingredients": [\n    {\n      "item": "minecraft:tuff"\n    },\n    {\n      "item": "minecraft:granite"\n    },\n    {\n      "fluid": "minecraft:lava",\n      "nbt": {},\n      "amount": 15000\n    }\n  ],\n  "results": [\n    {\n      "item": "create:ochrum",\n      "count": 2\n    }\n  ]\n}')

    # add `red_sand_mixing.json`
    with open(os.path.join(TEMP, 'Create/src/main/resources/data/create/recipes/lenamerkli/red_sand_mixing.json'), 'w') as file:
        file.write('{\n  "type": "create:mixing",\n  "ingredients": [\n    {\n      "item": "minecraft:sand"\n    },\n    {\n      "fluid": "minecraft:lava",\n      "nbt": {},\n      "amount": 3000\n    }\n  ],\n  "results": [\n    {\n      "item": "minecraft:red_sand"\n    }\n  ]\n}')

    # add `redstone_dust_crushing.json`
    with open(os.path.join(TEMP, 'Create/src/main/resources/data/create/recipes/lenamerkli/redstone_dust_crushing.json'), 'w') as file:
        file.write('{\n  "type": "create:crushing",\n  "ingredients": [\n    {\n      "item": "create:veridium"\n    }\n  ],\n  "processingTime": 250,\n  "results": [\n    {\n      "chance": 0.25,\n      "item": "minecraft:redstone"\n    },\n    {\n      "chance": 0.5,\n      "item": "minecraft:tuff"\n    },\n    {\n      "chance": 0.5,\n      "item": "create:limestone"\n    }\n  ]\n}')

    # add `tuff_mixing.json`
    with open(os.path.join(TEMP, 'Create/src/main/resources/data/create/recipes/lenamerkli/tuff_mixing.json'), 'w') as file:
        file.write('{\n  "type": "create:mixing",\n  "ingredients": [\n    {\n      "item": "minecraft:cobblestone"\n    },\n    {\n      "item": "minecraft:gravel"\n    },\n    {\n      "fluid": "minecraft:lava",\n      "nbt": {},\n      "amount": 8000\n    }\n  ],\n  "results": [\n    {\n      "item": "minecraft:tuff"\n    }\n  ]\n}')

    # add `veridium_compacting.json`
    with open(os.path.join(TEMP, 'Create/src/main/resources/data/create/recipes/lenamerkli/veridium_compacting.json'), 'w') as file:
        file.write('{\n  "type": "create:compacting",\n  "ingredients": [\n    {\n      "item": "minecraft:tuff"\n    },\n    {\n      "item": "create:limestone"\n    },\n    {\n      "fluid": "minecraft:lava",\n      "nbt": {},\n      "amount": 12000\n    }\n  ],\n  "results": [\n    {\n      "item": "create:veridium",\n      "count": 2\n    }\n  ]\n}')

    # build
    subprocess.run(['./gradlew', 'build'], cwd=os.path.join(TEMP, 'Create'), check=True, stdout=None)

    # make dir
    pathlib.Path('~/Desktop/create_plusplus/').expanduser().mkdir(parents=True, exist_ok=True)

    # copy jar
    file_list = os.listdir(os.path.join(TEMP, 'Create/build/libs/'))
    file = None
    for f in file_list:
        if f.endswith('.jar') and 'source' not in f:
            file = f
    if file is None:
        raise RuntimeError('No jar file found')
    subprocess.run(['cp', os.path.join(TEMP, 'Create/build/libs/', file), os.path.join(pathlib.Path('~/Desktop/create_plusplus/').expanduser(), file)], check=True, stdout=None)
