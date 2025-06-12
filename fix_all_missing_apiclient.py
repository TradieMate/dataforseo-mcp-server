#!/usr/bin/env python3

import os
import re
import glob

def fix_all_register_tool_calls(content):
    """Fix all registerTool calls that are missing apiClient parameter"""
    
    # Use regex to find and fix all registerTool calls
    # Pattern: registerTool(...) that doesn't end with , apiClient)
    
    def replace_register_tool(match):
        full_match = match.group(0)
        
        # Check if it already has apiClient
        if ', apiClient)' in full_match:
            return full_match
        
        # Add apiClient before the final closing parenthesis
        # Find the last ) and replace with , apiClient)
        if full_match.endswith(');'):
            return full_match[:-2] + ', apiClient);'
        elif full_match.endswith(')'):
            return full_match[:-1] + ', apiClient)'
        else:
            return full_match
    
    # Pattern to match registerTool calls (multi-line)
    # This is a complex pattern that matches the entire registerTool call
    pattern = r'registerTool\s*\(\s*server,\s*"[^"]+",\s*\{[^}]*\},\s*async\s*\([^)]*\)\s*=>\s*\{[^}]*\}\s*\)'
    
    # For simpler cases, let's use a different approach
    # Split by lines and process each registerTool call
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
            if ', apiClient)' not in full_call:
                # Find the last line that ends with ) or );
                call_lines_copy = call_lines[:]
                last_line = call_lines_copy[-1]
                
                if last_line.strip().endswith(');'):
                    call_lines_copy[-1] = last_line.replace(');', ', apiClient);')
                elif last_line.strip().endswith(')'):
                    call_lines_copy[-1] = last_line.replace(')', ', apiClient)')
                else:
                    # Try to find ) in the last few lines
                    for k in range(len(call_lines_copy) - 1, -1, -1):
                        if ')' in call_lines_copy[k]:
                            if call_lines_copy[k].strip().endswith(');'):
                                call_lines_copy[k] = call_lines_copy[k].replace(');', ', apiClient);')
                            elif call_lines_copy[k].strip().endswith(')'):
                                call_lines_copy[k] = call_lines_copy[k].replace(')', ', apiClient)')
                            break
                
                result_lines.extend(call_lines_copy)
            else:
                result_lines.extend(call_lines)
            
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
    content = fix_all_register_tool_calls(content)
    
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