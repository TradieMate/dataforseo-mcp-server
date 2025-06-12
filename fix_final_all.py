#!/usr/bin/env python3

import os
import re
import glob

def fix_register_tool_calls_final(content):
    """Final comprehensive fix for all registerTool calls"""
    
    # Pattern to match registerTool calls that are missing apiClient
    # Look for registerTool calls that end with just ) instead of , apiClient)
    
    lines = content.split('\n')
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this line starts a registerTool call
        if 'registerTool(' in line and 'server,' in line:
            # Collect the entire call
            call_lines = [line]
            paren_count = line.count('(') - line.count(')')
            j = i + 1
            
            # Continue collecting lines until we have balanced parentheses
            while paren_count > 0 and j < len(lines):
                call_lines.append(lines[j])
                paren_count += lines[j].count('(') - lines[j].count(')')
                j += 1
            
            # Join the call back together
            full_call = '\n'.join(call_lines)
            
            # Check if this call needs apiClient added
            if not re.search(r',\s*apiClient\s*\)\s*;?\s*$', full_call.strip()):
                # Add apiClient before the final closing parenthesis
                full_call = re.sub(r'\)\s*;?\s*$', ', apiClient);', full_call.strip())
            
            # Add the fixed call to results
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
    content = fix_register_tool_calls_final(content)
    
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