from cryptography.fernet import Fernet

# Generate a new secret key
secret_key = Fernet.generate_key()

# Convert the bytes key to a string (optional, but can be useful for storage)
secret_key_str = secret_key.decode()

print("Generated Secret Key:", secret_key_str)