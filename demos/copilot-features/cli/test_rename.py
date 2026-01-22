import pytest
import os
import tempfile
import shutil
from pathlib import Path
import sys
from rename import rename_chroma_to_chroma, print_summary_table


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    # Cleanup
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_files(temp_dir):
    """Create sample files with chroma_ patterns."""
    # Create Python file with chroma_ content
    py_file = Path(temp_dir) / "chroma_service.py"
    py_file.write_text("""
def chroma_add_item(item):
    chroma_list.append(item)

chroma_config = {}
""")
    
    # Create YAML config file
    yaml_file = Path(temp_dir) / "chroma_config.yaml"
    yaml_file.write_text("""
chroma_api_key: secret
chroma_timeout: 30
""")
    
    # Create markdown file
    md_file = Path(temp_dir) / "README.md"
    md_file.write_text("# Globex Service\nThe chroma_service module handles requests.")
    
    # Create binary file (should be skipped)
    bin_file = Path(temp_dir) / "chroma_image.bin"
    bin_file.write_bytes(b'\x89PNG\r\n\x1a\n' + b'chroma_' * 10)
    
    # Create subdirectory to test recursion
    sub_dir = Path(temp_dir) / "chroma_subdir"
    sub_dir.mkdir()
    sub_file = sub_dir / "chroma_handler.py"
    sub_file.write_text("class GlobexHandler: pass")
    
    return temp_dir


def test_rename_files(sample_files):
    """Test that files with chroma_ in name are renamed."""
    rename_log, stats = rename_chroma_to_chroma(sample_files)
    
    # Check that files were renamed
    assert stats['files_renamed'] >= 2
    assert not Path(sample_files, "chroma_service.py").exists()
    assert Path(sample_files, "chroma_service.py").exists()
    assert not Path(sample_files, "chroma_config.yaml").exists()
    assert Path(sample_files, "chroma_config.yaml").exists()


def test_rename_file_content(sample_files):
    """Test that file contents are updated with chroma_ → chroma_."""
    rename_log, stats = rename_chroma_to_chroma(sample_files)
    
    # Check Python file content
    py_file = Path(sample_files) / "chroma_service.py"
    content = py_file.read_text()
    assert 'chroma_add_item' in content
    assert 'chroma_list' in content
    assert 'chroma_' not in content
    
    # Check YAML file content
    yaml_file = Path(sample_files) / "chroma_config.yaml"
    content = yaml_file.read_text()
    assert 'chroma_api_key' in content
    assert 'chroma_timeout' in content
    assert 'chroma_' not in content


def test_skip_binary_files(sample_files):
    """Test that binary files are not processed."""
    bin_file = Path(sample_files) / "chroma_image.bin"
    original_content = bin_file.read_bytes()
    
    rename_log, stats = rename_chroma_to_chroma(sample_files)
    
    # Binary file should not be renamed or modified
    assert bin_file.exists()
    assert bin_file.read_bytes() == original_content


def test_skip_git_and_node_modules(temp_dir):
    """Test that .git and node_modules directories are skipped."""
    # Create .git directory with globex file
    git_dir = Path(temp_dir) / ".git"
    git_dir.mkdir()
    git_file = git_dir / "chroma_config"
    git_file.write_text("chroma_data")
    
    # Create node_modules directory with globex file
    nm_dir = Path(temp_dir) / "node_modules"
    nm_dir.mkdir()
    nm_file = nm_dir / "chroma_package.js"
    nm_file.write_text("const globex = {}")
    
    rename_log, stats = rename_chroma_to_chroma(temp_dir)
    
    # These directories should not be processed
    assert git_file.exists()
    assert not Path(git_dir, "chroma_config").exists()
    assert nm_file.exists()
    assert not Path(nm_dir, "chroma_package.js").exists()


def test_recursive_directory_traversal(sample_files):
    """Test that subdirectories are processed recursively."""
    rename_log, stats = rename_chroma_to_chroma(sample_files)
    
    # Check subdirectory file was renamed
    assert not Path(sample_files, "chroma_subdir", "chroma_handler.py").exists()
    assert Path(sample_files, "chroma_subdir", "chroma_handler.py").exists()


def test_stats_tracking(sample_files):
    """Test that statistics are tracked correctly."""
    rename_log, stats = rename_chroma_to_chroma(sample_files)
    
    assert stats['files_renamed'] > 0
    assert stats['files_updated'] > 0
    assert stats['symbols_replaced'] > 0
    assert len(stats['errors']) == 0


def test_no_errors_on_valid_files(sample_files):
    """Test that no errors occur on valid files."""
    rename_log, stats = rename_chroma_to_chroma(sample_files)
    
    assert len(stats['errors']) == 0


def test_rename_log_structure(sample_files):
    """Test that rename log has correct structure."""
    rename_log, stats = rename_chroma_to_chroma(sample_files)
    
    # Check that log entries have required fields
    for log in rename_log:
        assert 'type' in log
        assert 'status' in log
        if log['type'] == 'FILE':
            assert 'old_name' in log
            assert 'new_name' in log
        elif log['type'] == 'CONTENT':
            assert 'file' in log
            assert 'replacements' in log


def test_multiple_replacements_in_file(temp_dir):
    """Test file with multiple chroma_ occurrences."""
    py_file = Path(temp_dir) / "test.py"
    py_file.write_text("""
class GlobexManager:
    def __init__(self):
        self.chroma_config = {}
        self.chroma_cache = []
        self.chroma_timeout = 30
""")
    
    rename_log, stats = rename_chroma_to_chroma(temp_dir)
    
    # Should replace 4 occurrences
    assert stats['symbols_replaced'] >= 4
    content = py_file.read_text()
    assert 'chroma_' not in content
    assert 'chroma_' in content


def test_mixed_case_preservation(temp_dir):
    """Test that only chroma_ (lowercase) is replaced."""
    py_file = Path(temp_dir) / "test.py"
    py_file.write_text("""
# Globex is a company
GLOBEX_CONSTANT = 1
chroma_var = 2
""")
    
    rename_log, stats = rename_chroma_to_chroma(temp_dir)
    content = py_file.read_text()
    
    # Only chroma_ should be replaced, not Globex or GLOBEX_
    assert 'Globex is a company' in content
    assert 'GLOBEX_CONSTANT' in content
    assert 'chroma_var' in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
