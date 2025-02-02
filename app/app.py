import base64
import time

def encrypt_data(data):
    # Dummy encryption: Base64 encoding (for demonstration only)
    return base64.b64encode(data.encode()).decode()

# PCI-DSS Requirement: Masked PAN in logs
print("Processing card: ****-****-****-1111")  # Masked Primary Account Number

# Simulate a transaction process that requires encryption
transaction = "TXN1234567890"
encrypted_transaction = encrypt_data(transaction)
print("Encrypted Transaction: " + encrypted_transaction)

# Keep the container running for compliance checks
time.sleep(6)  # sleeps for 10 minutes
