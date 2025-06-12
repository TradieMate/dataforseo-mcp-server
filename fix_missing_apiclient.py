#!/usr/bin/env python3

import os
import re
import glob

def fix_missing_apiclient(content):
    """Fix registerTool calls that are missing the apiClient parameter"""
    
    lines = content.split('\n')
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this line starts a registerTool call
        if 'registerTool(' in line and 'server,' in line:
            # Find the matching closing parenthesis
            paren_count = line.count('(') - line.count(')')
            full_call = line
            j = i + 1
            
            while paren_count > 0 and j < len(lines):
                full_call += '\n' + lines[j]
                paren_count += lines[j].count('(') - lines[j].count(')')
                j += 1
            
            # Check if this call is missing apiClient
            if ', apiClient)' not in full_call:
                # Find the last closing parenthesis and add apiClient before it
                last_paren_pos = full_call.rfind(')')
                if last_paren_pos != -1:
                    # Add apiClient before the closing parenthesis
                    fixed_call = full_call[:last_paren_pos] + ', apiClient)'
                    
                    # Split the fixed call back into lines
                    fixed_lines = fixed_call.split('\n')
                    result_lines.extend(fixed_lines)
                else:
                    # If we can't find the closing paren, just add the original
                    result_lines.extend(full_call.split('\n'))
            else:
                # Already has apiClient, add as is
                result_lines.extend(full_call.split('\n'))
            
            i = j
        else:
            result_lines.append(line)
            i += 1
    
    return '\n'.join(result_lines)

def process_file(filepath):
    """Process a single TypeScript file"""
    print(f"Processing {filepath}")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Apply fixes
    content = fix_missing_apiclient(content)
    
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