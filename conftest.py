"""
Pytest configuration for Zac tests.
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def test_db_path():
    """Path for test database."""
    return "test_zac.db"


@pytest.fixture(autouse=True)
def cleanup_test_db(test_db_path):
    """Clean up test database after tests."""
    yield
    
    # Cleanup
    import os
    if os.path.exists(test_db_path):
        os.remove(test_db_path)


@pytest.fixture(scope="session")
def anyio_backend():
    """Configure anyio backend for async tests."""
    return "asyncio"
