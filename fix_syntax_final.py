#!/usr/bin/env python3

import os
import re
import glob

def fix_syntax_errors(content):
    """Fix syntax errors caused by incorrect regex replacements"""
    
    # Fix z.string(, apiClient) -> z.string()
    content = re.sub(r'z\.string\(\s*,\s*apiClient\s*\)', 'z.string()', content)
    content = re.sub(r'z\.number\(\s*,\s*apiClient\s*\)', 'z.number()', content)
    content = re.sub(r'z\.boolean\(\s*,\s*apiClient\s*\)', 'z.boolean()', content)
    content = re.sub(r'z\.array\(\s*,\s*apiClient\s*\)', 'z.array()', content)
    content = re.sub(r'z\.enum\(\s*,\s*apiClient\s*\)', 'z.enum()', content)
    content = re.sub(r'z\.any\(\s*,\s*apiClient\s*\)', 'z.any()', content)
    
    # Fix any other z.type(, apiClient) patterns
    content = re.sub(r'z\.\w+\(\s*,\s*apiClient\s*\)', lambda m: m.group(0).replace(', apiClient', ''), content)
    
    return content

def process_file(filepath):
    """Process a single TypeScript file"""
    print(f"Processing {filepath}")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Apply syntax fixes
    content = fix_syntax_errors(content)
    
    # Only write if content changed
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  Fixed syntax in {filepath}")
        return True
    else:
        print(f"  No syntax fixes needed for {filepath}")
        return False

def main():
    # Find all TypeScript files in src/api
    api_files = glob.glob("src/api/**/*.ts", recursive=True)
    
    updated_files = []
    for filepath in api_files:
        if process_file(filepath):
            updated_files.append(filepath)
    
    print(f"\nFixed syntax in {len(updated_files)} files:")
    for f in updated_files:
        print(f"  {f}")

if __name__ == "__main__":
    main()