#!/usr/bin/env python3

import os
import re
import glob

def fix_file_completely(content):
    """Completely fix a file's registerTool calls and handler signatures"""
    
    # Step 1: Fix broken handler signatures like "async (params) => , apiClient) => {"
    content = re.sub(r'async \(([^)]*)\) => , apiClient\) => \{', r'async (\1, client) => {', content)
    
    # Step 2: Fix handler signatures that are missing client parameter
    # Pattern: async (params) => { ... client.something
    def fix_handler_signature(match):
        handler = match.group(0)
        if 'client.' in handler and 'async (params)' in handler:
            return handler.replace('async (params)', 'async (params, client)')
        elif 'client.' in handler and 'async (_params)' in handler:
            return handler.replace('async (_params)', 'async (_params, client)')
        return handler
    
    # Apply handler signature fixes
    content = re.sub(r'async \([^)]*\) => \{[^}]*client\.[^}]*\}', fix_handler_signature, content, flags=re.DOTALL)
    
    # Step 3: Fix registerTool calls with wrong parameter order
    # Pattern: }, apiClient, async ( -> }, async (, and move apiClient to end
    def fix_register_tool_order(match):
        full_match = match.group(0)
        if '}, apiClient,' in full_match and 'async (' in full_match:
            # Remove apiClient from middle
            fixed = full_match.replace('}, apiClient,', '},')
            # Add apiClient at the end
            if fixed.endswith(')'):
                fixed = fixed[:-1] + ', apiClient)'
            elif fixed.endswith(');'):
                fixed = fixed[:-2] + ', apiClient);'
            return fixed
        return full_match
    
    content = re.sub(r'registerTool\s*\([^;]*?\);?', fix_register_tool_order, content, flags=re.DOTALL)
    
    # Step 4: Fix registerTool calls missing apiClient parameter
    def fix_missing_apiclient(match):
        full_match = match.group(0)
        comma_count = full_match.count(',')
        
        # If it has exactly 3 commas and doesn't have apiClient, add it
        if comma_count == 3 and ', apiClient' not in full_match:
            if full_match.endswith(')'):
                return full_match[:-1] + ', apiClient)'
            elif full_match.endswith(');'):
                return full_match[:-2] + ', apiClient);'
        
        return full_match
    
    content = re.sub(r'registerTool\s*\([^;]*?\);?', fix_missing_apiclient, content, flags=re.DOTALL)
    
    # Step 5: Fix syntax errors in Zod schemas
    content = re.sub(r'z\.string\(\s*,\s*apiClient\s*\)', 'z.string()', content)
    content = re.sub(r'z\.number\(\s*,\s*apiClient\s*\)', 'z.number()', content)
    content = re.sub(r'z\.boolean\(\s*,\s*apiClient\s*\)', 'z.boolean()', content)
    content = re.sub(r'z\.array\(\s*,\s*apiClient\s*\)', 'z.array()', content)
    content = re.sub(r'z\.enum\(\s*,\s*apiClient\s*\)', 'z.enum()', content)
    content = re.sub(r'z\.any\(\s*,\s*apiClient\s*\)', 'z.any()', content)
    
    # Step 6: Fix duplicate apiClient parameters
    content = re.sub(r',\s*apiClient\s*,\s*apiClient\s*\)', ', apiClient)', content)
    
    # Step 7: Fix extra parameters
    content = re.sub(r',\s*client\s*\)', ')', content)
    
    # Step 8: Fix cases where apiClient is used instead of client in handler bodies
    # Replace apiClient.get/post with client.get/post in handler bodies
    content = re.sub(r'await apiClient\.(get|post)', r'await client.\1', content)
    
    return content

def process_file(filepath):
    """Process a single TypeScript file"""
    print(f"Processing {filepath}")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Apply comprehensive fixes
    content = fix_file_completely(content)
    
    # Only write if content changed
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  Fixed {filepath}")
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
    
    print(f"\nFixed {len(updated_files)} files:")
    for f in updated_files:
        print(f"  {f}")

if __name__ == "__main__":
    main()