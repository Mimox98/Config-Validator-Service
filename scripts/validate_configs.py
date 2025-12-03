#Validation script for Jenkins pipeline.
#Validates all config files and exits with proper status code.
import sys
from app.core.validator import ConfigValidator

def main():
    validator = ConfigValidator()
    results = validator.validate_all_configs()
    
    print('\n=== Configuration Validation Results ===')
    
    all_valid = True
    for result in results:
        if "error" in result:
            print(f'✗ ERROR: {result["error"]}')
            all_valid = False
            continue
        
        if "warning" in result:
            print(f'⚠ WARNING: {result["warning"]}')
            continue
        
        status = "✓ PASS" if result.get("valid", False) else "✗ FAIL"
        print(f'{status}: {result["file"]}')
        
        if not result.get("valid", False):
            all_valid = False
            for error in result.get("errors", []):
                print(f'  - {error}')
    
    if all_valid:
        print('\n✓ All configurations are valid!')
        sys.exit(0)
    else:
        print('\n✗ Validation FAILED')
        sys.exit(1)

if __name__ == '__main__':
    main()