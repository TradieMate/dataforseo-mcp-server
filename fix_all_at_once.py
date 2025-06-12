#!/usr/bin/env python3

import os
import re
import glob

def fix_register_tool_calls_comprehensive(content):
    """Fix all registerTool calls that are missing apiClient parameter"""
    
    # Use regex to find all registerTool calls and fix them
    # Pattern to match registerTool calls that end with } followed by );
    
    # This pattern matches:
    # registerTool(
    #   server,
    #   "name",
    #   schema,
    #   async (params) => {
    #     ...
    #   }
    # );
    
    pattern = r'(registerTool\s*\(\s*server,\s*"[^"]+",\s*[^,]+,\s*async\s*\([^)]*\)\s*=>\s*\{[^}]*\})\s*\)\s*;'
    
    def replace_func(match):
        # Add apiClient before the closing );
        return match.group(1) + ',\n    apiClient\n  );'
    
    # Apply the replacement
    result = re.sub(pattern, replace_func, content, flags=re.MULTILINE | re.DOTALL)
    
    # Also handle cases where the function body spans multiple lines
    # More complex pattern for multi-line function bodies
    pattern2 = r'(registerTool\s*\(\s*server,\s*"[^"]+",\s*[^,]+,\s*async\s*\([^)]*\)\s*=>\s*\{(?:[^{}]|\{[^}]*\})*\})\s*\)\s*;'
    
    result = re.sub(pattern2, replace_func, result, flags=re.MULTILINE | re.DOTALL)
    
    return result

def process_file(filepath):
    """Process a single TypeScript file"""
    print(f"Processing {filepath}")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Apply fixes
    content = fix_register_tool_calls_comprehensive(content)
    
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