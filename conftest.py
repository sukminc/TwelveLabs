import os
import pytest
from twelvelabs import TwelveLabs
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


@pytest.fixture(scope="session")
def client():
    """Returns an authenticated Twelve Labs API client."""
    api_key = os.getenv("TWELVE_LABS_API_KEY")
    if not api_key:
        pytest.fail("TWELVE_LABS_API_KEY environment variable not set.")
    return TwelveLabs(api_key=api_key)


@pytest.fixture(scope="session")
def index_id():
    """Returns the ID of the test index."""
    index = os.getenv("TWELVE_LABS_INDEX_ID")
    if not index:
        pytest.fail("TWELVE_LABS_INDEX_ID environment variable not set.")
    return index
