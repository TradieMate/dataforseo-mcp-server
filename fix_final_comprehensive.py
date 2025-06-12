#!/usr/bin/env python3

import os
import re
import glob

def fix_register_tool_calls_comprehensive(content):
    """Fix all registerTool calls comprehensively"""
    
    # First, let's find all registerTool calls and fix them one by one
    # Pattern to match registerTool calls that span multiple lines
    
    # Split into lines for easier processing
    lines = content.split('\n')
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this line contains registerTool
        if 'registerTool(' in line:
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
            
            # Fix this specific call
            fixed_call = fix_single_call(full_call)
            
            # Add the fixed call to results
            result_lines.extend(fixed_call.split('\n'))
            i = j
        else:
            result_lines.append(line)
            i += 1
    
    return '\n'.join(result_lines)

def fix_single_call(call_text):
    """Fix a single registerTool call"""
    
    # Check if it already has apiClient at the end
    if re.search(r',\s*apiClient\s*\)\s*;?\s*$', call_text.strip()):
        return call_text
    
    # Check if it has apiClient in the wrong place (as a parameter to the handler)
    if 'async (_params, client)' in call_text or 'async (params, client)' in call_text:
        # Replace client with apiClient in the handler
        call_text = re.sub(r'async\s*\([^,]+,\s*client\)', 'async (params)', call_text)
    
    # Remove any existing misplaced apiClient
    call_text = re.sub(r'},\s*apiClient\)', '})', call_text)
    
    # Find the last closing parenthesis and add apiClient before it
    # But make sure we're not inside a function body
    
    # Find the end of the call (should end with ); or ))
    if call_text.strip().endswith(');'):
        call_text = call_text.rstrip(');') + ', apiClient);'
    elif call_text.strip().endswith(')'):
        call_text = call_text.rstrip(')') + ', apiClient)'
    else:
        # Try to find the closing pattern
        call_text = re.sub(r'\)\s*;?\s*$', ', apiClient);', call_text)
    
    return call_text

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