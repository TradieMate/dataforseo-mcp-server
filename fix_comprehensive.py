#!/usr/bin/env python3

import os
import re
import glob

def fix_register_tool_calls(content):
    """Fix all registerTool calls to have the correct signature"""
    
    # Pattern to match registerTool calls
    # This handles multi-line calls
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
            
            # Now fix the call
            fixed_call = fix_single_register_tool_call(full_call)
            
            # Split the fixed call back into lines
            fixed_lines = fixed_call.split('\n')
            result_lines.extend(fixed_lines)
            i = j
        else:
            result_lines.append(line)
            i += 1
    
    return '\n'.join(result_lines)

def fix_single_register_tool_call(call_text):
    """Fix a single registerTool call"""
    
    # Extract the parts of the call
    # Pattern: registerTool(server, "name", schema, handler, [apiClient])
    
    # If it already has apiClient in the right place, return as is
    if ', apiClient)' in call_text and call_text.count('apiClient') == 1:
        return call_text
    
    # Remove any existing apiClient that's in the wrong place
    call_text = re.sub(r',\s*apiClient\)', ')', call_text)
    call_text = re.sub(r'},\s*apiClient\)', '})', call_text)
    
    # Find the last closing parenthesis and add apiClient before it
    last_paren_pos = call_text.rfind(')')
    if last_paren_pos != -1:
        # Check if there's already a comma before the closing paren
        before_paren = call_text[:last_paren_pos].rstrip()
        if before_paren.endswith(','):
            # Remove the trailing comma and add apiClient
            call_text = before_paren[:-1] + ', apiClient)'
        else:
            # Add comma and apiClient
            call_text = call_text[:last_paren_pos] + ', apiClient)'
    
    return call_text

def fix_client_references(content, filename):
    """Fix undefined client references"""
    
    # For most files, replace 'client.' with 'apiClient.'
    if 'localfalcon' not in filename.lower():
        content = re.sub(r'\bclient\.', 'apiClient.', content)
    else:
        # For localfalcon, we need to be more careful
        # Replace 'client.' with 'client.' but ensure client is defined
        if 'const client = new LocalFalconClient' not in content:
            # If client is not defined, replace with apiClient
            content = re.sub(r'\bclient\.', 'apiClient.', content)
    
    return content

def fix_handler_signatures(content):
    """Fix handler function signatures that have apiClient in wrong place"""
    
    # Pattern to find handlers that have apiClient as the handler function
    # registerTool(server, "name", schema, apiClient, actual_handler)
    pattern = r'registerTool\(\s*server,\s*"[^"]+",\s*\{[^}]*\},\s*apiClient,\s*async\s*\([^)]*\)\s*=>\s*\{'
    
    def fix_handler(match):
        # Extract the matched text and fix it
        text = match.group(0)
        # Move apiClient to the end
        text = text.replace(', apiClient,', ',')
        text = text.rstrip('{') + ', apiClient) => {'
        return text
    
    content = re.sub(pattern, fix_handler, content, flags=re.MULTILINE | re.DOTALL)
    
    return content

def process_file(filepath):
    """Process a single TypeScript file"""
    print(f"Processing {filepath}")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Apply fixes
    content = fix_register_tool_calls(content)
    content = fix_client_references(content, filepath)
    content = fix_handler_signatures(content)
    
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