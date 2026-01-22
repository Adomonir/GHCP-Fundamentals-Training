import os
import re
from pathlib import Path
from collections import defaultdict

def rename_chroma_to_chroma(root_dir="."):
    """
    Recursively rename files and symbols from 'chroma_' to 'chroma_'.
    Skips .git and node_modules directories.
    """
    
    stats = {
        'files_renamed': 0,
        'files_updated': 0,
        'symbols_replaced': 0,
        'errors': []
    }
    
    rename_log = []
    
    # Directories to skip
    skip_dirs = {'.git', 'node_modules', '__pycache__', '.pytest_cache', '.venv', 'venv'}
    
    # File extensions to process
    text_extensions = {'.py', '.yaml', '.yml', '.md', '.txt', '.json', '.toml', '.cfg', '.ini'}
    
    # Walk directory tree
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter out skip directories
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        
        # Process files
        for filename in filenames:
            filepath = Path(dirpath) / filename
            
            # Rename file if it contains 'chroma_'
            if 'chroma_' in filename:
                new_filename = filename.replace('chroma_', 'chroma_')
                new_filepath = Path(dirpath) / new_filename
                
                try:
                    filepath.rename(new_filepath)
                    rename_log.append({
                        'type': 'FILE',
                        'old_name': filename,
                        'new_name': new_filename,
                        'status': 'SUCCESS'
                    })
                    stats['files_renamed'] += 1
                    filepath = new_filepath
                except Exception as e:
                    stats['errors'].append(f"Failed to rename {filepath}: {str(e)}")
                    rename_log.append({
                        'type': 'FILE',
                        'old_name': filename,
                        'new_name': 'N/A',
                        'status': f'ERROR: {str(e)}'
                    })
            
            # Update file contents if text file
            if filepath.suffix in text_extensions:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Count replacements
                    new_content, count = re.subn(r'chroma_', 'chroma_', content)
                    
                    if count > 0:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        rename_log.append({
                            'type': 'CONTENT',
                            'file': filepath.name,
                            'replacements': count,
                            'status': 'SUCCESS'
                        })
                        stats['files_updated'] += 1
                        stats['symbols_replaced'] += count
                
                except Exception as e:
                    stats['errors'].append(f"Failed to update {filepath}: {str(e)}")
    
    return rename_log, stats

def print_summary_table(rename_log, stats):
    """Print a formatted summary table of all changes."""
    
    print("\n" + "="*80)
    print("GLOBEX TO CHROMA RENAME SUMMARY".center(80))
    print("="*80 + "\n")
    
    # Summary statistics
    print("STATISTICS:")
    print(f"  Files Renamed:      {stats['files_renamed']}")
    print(f"  Files Updated:      {stats['files_updated']}")
    print(f"  Symbols Replaced:   {stats['symbols_replaced']}")
    if stats['errors']:
        print(f"  Errors:             {len(stats['errors'])}")
    print()
    
    # File renames table
    file_renames = [log for log in rename_log if log['type'] == 'FILE']
    if file_renames:
        print("FILE RENAMES:")
        print(f"{'Old Name':<40} {'New Name':<40} {'Status':<10}")
        print("-" * 90)
        for log in file_renames:
            print(f"{log['old_name']:<40} {log['new_name']:<40} {log['status']:<10}")
        print()
    
    # Content updates table
    content_updates = [log for log in rename_log if log['type'] == 'CONTENT']
    if content_updates:
        print("CONTENT UPDATES:")
        print(f"{'File Name':<40} {'Replacements':<15} {'Status':<10}")
        print("-" * 65)
        for log in content_updates:
            print(f"{log['file']:<40} {log['replacements']:<15} {log['status']:<10}")
        print()
    
    # Errors
    if stats['errors']:
        print("ERRORS:")
        for error in stats['errors']:
            print(f"  ❌ {error}")
        print()
    
    print("="*80)

if __name__ == "__main__":
    root_directory = "."
    rename_log, stats = rename_chroma_to_chroma(root_directory)
    print_summary_table(rename_log, stats)