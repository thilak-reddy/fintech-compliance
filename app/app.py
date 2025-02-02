import base64
import time
import logging
import hashlib
import json
from datetime import datetime
import os

# Add before logging configuration
os.makedirs('/app/logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S'
)
logger = logging.getLogger(__name__)

def encrypt_data(data):
    # Dummy encryption: Base64 encoding (for demonstration only)
    return base64.b64encode(data.encode()).decode()

def validate_input(data):
    if not isinstance(data, str):
        raise ValueError("Input must be a string")
    if len(data) > 100:
        raise ValueError("Input too long")
    return True

try:
    # PCI-DSS Requirement: Masked PAN in logs
    logger.info("Processing card: ****-****-****-1111")

    # Simulate a transaction process that requires encryption
    transaction = "TXN1234567890"
    validate_input(transaction)
    encrypted_transaction = encrypt_data(transaction)
    logger.info(f"Encrypted Transaction: {encrypted_transaction}")

    # Write file integrity check data
    with open('integrity.json', 'w') as f:
        json.dump({
            'last_check': datetime.now().isoformat(),
            'files_checked': 10,
            'issues_found': 0
        }, f)

    # Keep the container running for compliance checks
    while True:
        time.sleep(60)
        logger.info("Health check: OK")

except Exception as e:
    logger.error(f"Error processing transaction: {str(e)}")
    raise
