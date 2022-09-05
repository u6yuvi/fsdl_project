import pytest
from semsearch.load import load_corpus

@pytest.fixture()
def sample_input_data():
    return load_corpus()