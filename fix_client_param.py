#!/usr/bin/env python3

import os
import re
import glob

def fix_client_parameter(content):
    """Fix handler functions that use 'client' but don't have it as parameter"""
    
    # Pattern: async (params) => { ... client.something
    # Should be: async (params, client) => { ... client.something
    
    # Find all async function handlers that use client but don't have client parameter
    def fix_handler(match):
        handler = match.group(0)
        
        # Check if handler uses 'client.' but doesn't have 'client' as parameter
        if 'client.' in handler:
            if 'async (params) =>' in handler:
                return handler.replace('async (params) =>', 'async (params, client) =>')
            elif 'async (_params) =>' in handler:
                return handler.replace('async (_params) =>', 'async (_params, client) =>')
        
        return handler
    
    # Match async handlers that span multiple lines and use client
    content = re.sub(r'async \([^)]*\) => \{[^}]*?client\.[^}]*?\}', fix_handler, content, flags=re.DOTALL)
    
    return content

def process_file(filepath):
    """Process a single TypeScript file"""
    print(f"Processing {filepath}")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Apply client parameter fixes
    content = fix_client_parameter(content)
    
    # Only write if content changed
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  Fixed client parameters in {filepath}")
        return True
    else:
        print(f"  No client parameter fixes needed for {filepath}")
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
    
    print(f"\nFixed client parameters in {len(updated_files)} files:")
    for f in updated_files:
        print(f"  {f}")

if __name__ == "__main__":
    main()