"""Local fixtures for forum tests.

Adds a Flask test client that has a fresh database per test,
without touching the global conftest.
"""

import pytest


@pytest.fixture
def client(application, database):
    """A Flask test client with a fresh database per test."""
    return application.test_client()