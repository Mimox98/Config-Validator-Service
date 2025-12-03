#Unit tests for the ConfigValidator.
import pytest
from app.core.validator import ConfigValidator

@pytest.fixture
def validator():
    return ConfigValidator()

def test_valid_json_config(validator):
    #Test validation of a valid JSON configuration
    valid_config = """
    {
        "name": "test-service",
        "version": "1.0.0",
        "environment": "development"
    }
    """
    is_valid, errors = validator.validate_content(valid_config, "json")
    assert is_valid is True
    assert len(errors) == 0

def test_valid_yaml_config(validator):
    #Test validation of a valid YAML configuration
    valid_config = """
    name: test-service
    version: 1.0.0
    environment: production
    """
    is_valid, errors = validator.validate_content(valid_config, "yaml")
    assert is_valid is True
    assert len(errors) == 0

def test_missing_required_key(validator):
    invalid_config = """
    {
        "name": "test-service",
        "version": "1.0.0"
    }
    """
    is_valid, errors = validator.validate_content(invalid_config, "json")
    assert is_valid is False
    assert any("environment" in error for error in errors)

def test_invalid_environment(validator):
    invalid_config = """
    {
        "name": "test-service",
        "version": "1.0.0",
        "environment": "invalid-env"
    }
    """
    is_valid, errors = validator.validate_content(invalid_config, "json")
    assert is_valid is False
    assert any("Invalid environment" in error for error in errors)

def test_invalid_json(validator):
    #Test that malformed JSON is caught.
    invalid_json = '{"name": "test", invalid json}'
    is_valid, errors = validator.validate_content(invalid_json, "json")
    assert is_valid is False
    assert len(errors) > 0

def test_invalid_version_type(validator):
    #Test that non-string version values are rejected
    invalid_config = """
    {
        "name": "test-service",
        "version": 123,
        "environment": "development"
    }
    """
    is_valid, errors = validator.validate_content(invalid_config, "json")
    assert is_valid is False
    assert any("Version must be" in error for error in errors)

def test_unsupported_config_type(validator):
    #Test that unsupported config types are rejected
    config = '{"test": "data"}'
    is_valid, errors = validator.validate_content(config, "xml")
    assert is_valid is False
    assert any("Unsupported config type" in error for error in errors)
