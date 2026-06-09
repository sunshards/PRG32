import os
import re

docs_dir = "/Users/simoneboscaglia/Developer/PRG32/docs"
readme_file = "/Users/simoneboscaglia/Developer/PRG32/README.md"

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original_content = content

    # 1. Scripts
    content = content.replace('./scripts/qemu/build_qemu.sh', 'python3 -m prg32 qemu build-and-flash')
    content = content.replace('./scripts/qemu/launch_qemu.sh', 'python3 -m prg32 qemu launch')
    content = content.replace('./scripts/qemu/lauch_qemu.sh', 'python3 -m prg32 qemu launch')
    content = re.sub(r'\./scripts/qemu/qemu_inject_cartridge\.sh\s+([^\n\\]+)', r'python3 -m prg32 qemu upload \1', content)

    # 2. Upload QEMU (needs to drop --flash ...)
    content = re.sub(r'python3 tools/prg32_game\.py upload-qemu\s+([^\n]+?)\s+--flash\s+build-qemu/qemu_flash\.bin', r'python3 -m prg32 qemu upload \1', content)
    content = content.replace('python3 tools/prg32_game.py upload-qemu', 'python3 -m prg32 qemu upload')

    # 3. Build Firmware target
    content = content.replace('--firmware-elf build-esp32c6/PRG32.elf', '--target esp32c6')
    content = content.replace('--firmware-elf build-qemu/PRG32.elf', '--target qemu')

    # 4. Command name mappings
    content = content.replace('python3 tools/prg32_game.py build', 'python3 -m prg32 build-cartridge')
    content = content.replace('python3 tools/prg32_game.py upload', 'python3 -m prg32 esp32c6 upload-and-run') # Note: match `upload` but not `upload-qemu` because `upload-qemu` is already replaced
    content = content.replace('python3 tools/prg32_game.py doctor', 'python3 -m prg32 doctor')
    content = content.replace('python3 tools/prg32_game.py runtime', 'python3 -m prg32 runtime')
    
    # 5. General tools/prg32_game.py replacement (skip ignored)
    ignored_commands = ['attach-metadata', 'inspect-metadata', 'store-discover', 'store-list', 'store-download', 'publish', 'pack-bundle', 'publish-bundle']
    
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if 'tools/prg32_game.py' in line:
            if not any(cmd in line for cmd in ignored_commands):
                line = line.replace('tools/prg32_game.py', 'python3 -m prg32')
        new_lines.append(line)
        
    content = '\n'.join(new_lines)
    
    if content != original_content:
        print(f"Updated {filepath}")
        with open(filepath, 'w') as f:
            f.write(content)

for root, _, files in os.walk(docs_dir):
    for filename in files:
        if filename.endswith(".md"):
            filepath = os.path.join(root, filename)
            process_file(filepath)
            
process_file(readme_file)
print("Documentation replacement complete.")
