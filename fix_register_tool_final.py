#!/usr/bin/env python3

import os
import re
import glob

def fix_register_tool_calls(content):
    """Fix registerTool calls that are missing apiClient parameter"""
    
    # Split content into lines for easier processing
    lines = content.split('\n')
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Look for registerTool calls
        if 'registerTool(' in line and 'server,' in line:
            # This is the start of a registerTool call
            # Collect all lines until we find the closing parenthesis
            call_lines = [line]
            paren_count = line.count('(') - line.count(')')
            j = i + 1
            
            # Continue collecting lines until parentheses are balanced
            while paren_count > 0 and j < len(lines):
                call_lines.append(lines[j])
                paren_count += lines[j].count('(') - lines[j].count(')')
                j += 1
            
            # Now we have the complete registerTool call
            full_call = '\n'.join(call_lines)
            
            # Check if it already has apiClient
            if ', apiClient' in full_call:
                # Already has apiClient, keep as is
                result_lines.extend(call_lines)
            else:
                # Need to add apiClient
                # Find the line that ends the function (contains "}")
                # and the line that closes the call (contains ");")
                
                modified_lines = call_lines[:]
                
                # Look for the pattern:
                # }
                # );
                # and change it to:
                # },
                # apiClient
                # );
                
                for k in range(len(modified_lines) - 1):
                    if modified_lines[k].strip() == '}' and modified_lines[k + 1].strip() == ');':
                        # Found the pattern
                        modified_lines[k] = modified_lines[k].replace('}', '},')
                        modified_lines.insert(k + 1, '    apiClient')
                        break
                    elif modified_lines[k].strip() == '}' and modified_lines[k + 1].strip().startswith(')'):
                        # Found the pattern with possible extra content after )
                        modified_lines[k] = modified_lines[k].replace('}', '},')
                        modified_lines.insert(k + 1, '    apiClient')
                        break
                
                result_lines.extend(modified_lines)
            
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
    content = fix_register_tool_calls(content)
    
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