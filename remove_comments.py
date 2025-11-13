import re
import os
import glob

def remove_python_comments(content):
    lines = content.split('\n')
    cleaned_lines = []
    in_multiline_string = False
    
    for line in lines:
        stripped = line.lstrip()
        
        if '"""' in line or "'''" in line:
            quote_count = line.count('"""') + line.count("'''")
            if quote_count == 2:
                continue
            in_multiline_string = not in_multiline_string
            if not in_multiline_string:
                continue
            continue
        
        if in_multiline_string:
            continue
        
        if stripped.startswith('#'):
            continue
        
        if '#' in line and not ('"' in line or "'" in line):
            line = re.sub(r'\s*#.*$', '', line)
        
        if line.strip():
            cleaned_lines.append(line)
        elif cleaned_lines and cleaned_lines[-1].strip():
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def remove_js_comments(content):
    content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    
    lines = [line for line in content.split('\n') if line.strip()]
    return '\n'.join(lines)

backend_path = r"c:\Users\asus\OneDrive\Desktop\EE-PROJECT\HELP-X\helpx-backend"
frontend_path = r"c:\Users\asus\OneDrive\Desktop\EE-PROJECT\HELP-X\Frontend"

print("🧹 Removing comments from Python files...")
for py_file in glob.glob(os.path.join(backend_path, "*.py")):
    if "remove_comments.py" in py_file:
        continue
    
    with open(py_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cleaned = remove_python_comments(content)
    
    with open(py_file, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    
    print(f"  ✅ {os.path.basename(py_file)}")

print("\n🧹 Removing comments from JavaScript files...")
for js_file in glob.glob(os.path.join(frontend_path, "*.js")):
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cleaned = remove_js_comments(content)
    
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    
    print(f"  ✅ {os.path.basename(js_file)}")

print("\n✅ All comments removed successfully!")
