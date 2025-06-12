#!/usr/bin/env python3

import os
import re
import glob

def fix_malformed_handlers(content):
    """Fix malformed async handler signatures"""
    
    # Pattern to match: async (params) => , apiClient) => {
    # Replace with: async (params) => {
    pattern = r'async\s*\(params\)\s*=>\s*,\s*apiClient\)\s*=>\s*\{'
    replacement = r'async (params) => {'
    
    content = re.sub(pattern, replacement, content)
    
    return content

def process_file(filepath):
    """Process a single TypeScript file"""
    print(f"Processing {filepath}")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Apply fixes
    content = fix_malformed_handlers(content)
    
    # Only write if content changed
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  Updated {filepath}")
        return True
    else:
        print(f"  No changes needed for {filepath}")
        return False

def main():
    # Find all TypeScript files in src/api except tools.ts, client.ts, types.ts
    api_files = glob.glob("src/api/**/*.ts", recursive=True)
    exclude_files = {'tools.ts', 'client.ts', 'types.ts'}
    
    updated_files = []
    for filepath in api_files:
        filename = os.path.basename(filepath)
        if filename not in exclude_files:
            if process_file(filepath):
                updated_files.append(filepath)
    
    print(f"\nUpdated {len(updated_files)} files:")
    for f in updated_files:
        print(f"  {f}")

if __name__ == "__main__":
    main()