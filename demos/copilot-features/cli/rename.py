import os
import re
from pathlib import Path
from collections import defaultdict

def case_preserving_replace(match):
    """Replace 'globex' with 'chroma' while preserving the case pattern."""
    original = match.group(0)
    if original.isupper():
        return 'CHROMA'
    elif original[0].isupper():
        return 'Chroma'
    else:
        return 'chroma'

def rename_globex_to_chroma(root_dir="."):
    """
    Recursively rename files and symbols from 'globex' to 'chroma'.
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
    
    # First pass: collect directories to rename (bottom-up to avoid conflicts)
    dirs_to_rename = []
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # Filter out skip directories
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        
        for dirname in dirnames:
            if 'globex' in dirname.lower():
                old_dirpath = Path(dirpath) / dirname
                new_dirname = re.sub(r'globex', case_preserving_replace, dirname, flags=re.IGNORECASE)
                new_dirpath = Path(dirpath) / new_dirname
                dirs_to_rename.append((old_dirpath, new_dirpath, dirname, new_dirname))
    
    # Rename directories
    for old_path, new_path, old_name, new_name in dirs_to_rename:
        try:
            old_path.rename(new_path)
            rename_log.append({
                'type': 'DIR',
                'old_name': old_name,
                'new_name': new_name,
                'status': 'SUCCESS'
            })
            stats['files_renamed'] += 1
        except Exception as e:
            stats['errors'].append(f"Failed to rename directory {old_path}: {str(e)}")
    
    # Walk directory tree for files
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter out skip directories
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        
        # Process files
        for filename in filenames:
            filepath = Path(dirpath) / filename
            
            # Rename file if it contains 'globex'
            if 'globex' in filename.lower():
                new_filename = re.sub(r'globex', case_preserving_replace, filename, flags=re.IGNORECASE)
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
                    
                    # Count replacements - case preserving
                    new_content, count = re.subn(r'globex', case_preserving_replace, content, flags=re.IGNORECASE)
                    
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
    rename_log, stats = rename_globex_to_chroma(root_directory)
    print_summary_table(rename_log, stats)