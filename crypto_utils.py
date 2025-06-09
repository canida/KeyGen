from cryptography.fernet import Fernet
from dotenv import dotenv_values
import os
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('crypto_config.ini')

# Get file paths from config
key_file = config.get('paths', 'key_file', fallback='.env')



def generate_key():
    """
    Generate a new Fernet key.
    
    Returns:
        str: A base64 encoded key as a string.
    """
    return Fernet.generate_key().decode('utf-8')

def update_key_file(new_key_file):
    """
    Update the key file path in the configuration file.
    
    Args:
        new_key_file (str): The new file path for the key.
    """
    config.set('paths', 'key_file', new_key_file)
    with open('crypto_config.ini', 'w') as configfile:
        config.write(configfile)
    global key_file
    key_file = new_key_file


def get_key(filename=key_file):
    """
    Retrieve the key from a file.
    
    Args:
        filename (str): The file path where the key is stored.
        
    Returns:
        str: The key read from the file.
    """
    if filename != key_file and not os.path.exists(filename):
        raise FileNotFoundError(f"Error: The file {filename} does not exist. Please provide a valid file path.")
    if filename == key_file and not os.path.exists(key_file):
        raise FileNotFoundError(f"Error: The default key file {key_file} does not exist. Please save a key first.")    
    with open(filename, 'rb') as file:
        return file.read().decode('utf-8')

def save_key_to_file(key, file=key_file,create_dir=False, overwrite_file=True):
    """
    Save the provided key to a file.
    
    Args:
        key (str): The key to save.
        file (str): The full file path where the key will be saved.
    """
    try:
        dir_name = os.path.dirname(file)
        file_name = os.path.basename(file)

        # Check if a file names was provided
        if not file_name:
            raise ValueError("Error: No file name provided. Please specify a valid file name to save the key.")

        # Check if the given file is a directory
        if os.path.isdir(file):
            raise ValueError(f"Error: {file} is a directory, not a file. Please provide a valid file path.")

        # Check if directory was provided and if it exists
        if dir_name and not os.path.exists(dir_name):
            if create_dir:
                os.makedirs(dir_name, exist_ok=True)
            else:
                raise FileNotFoundError(f"Error: The directory for {file} does not exist. Please create it first.")
        # Check if the file already exists
        elif os.path.exists(file) and not overwrite_file:
            return
        
        # Write the key to the file
        with open(file, 'wb') as f:
            f.write(key.encode('utf-8'))
    except Exception as e:
        print(f"Error saving key to file: {e}")
        raise

def encrypt_data(data, key):
    """
    Encrypt data using the provided key.
    
    Args:
        data (str): The data to encrypt.
        key (str): The encryption key.
        
    Returns:
        str: The encrypted data as a base64 encoded string.
    """
    fernet = Fernet(key)
    return fernet.encrypt(data.encode('utf-8')).decode('utf-8')

def decrypt_data(encrypted_data, key):
    """
    Decrypt data using the provided key.
    
    Args:
        encrypted_data (str): The encrypted data to decrypt.
        key (str): The decryption key.
        
    Returns:
        str: The decrypted data as a string.
    """
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')




# Test the key generation and retrieval functions
print("Testing Key Generation and Retrieval with Config File")
key = generate_key()
print("Generated Key:", key)
#file = os.path.join(os.path.dirname(__file__), 'key_file.env')
#print("File:", file)
save_key_to_file(key)
print("Key_file:", key_file)

read_key = get_key()
print("Read Key:", read_key)
if read_key == key:
    print("Key successfully saved and retrieved.")
else:
    print("Error: The saved key does not match the generated key.")

print("Key generation and retrieval test completed.")
print("Testing Key Generation and Retrieval with given file")
key = generate_key()
print("Generated Key:", key)
save_key_to_file(key, file='test_key.env')
read_key = get_key('test_key.env')  
print("Read Key from test file:", read_key)
if read_key == key:
    print("Key successfully saved and retrieved from test file.")
else:
    print("Error: The saved key does not match the generated key from test file.")
print("Key generation and retrieval test with given file completed.")


print("Testing Key Generation and Retrieval provided file that does not exist")
key = generate_key()
print("Generated Key:", key)
save_key_to_file(key, file='./testDir/.env', create_dir=True, overwrite_file=True)
print("Attempted to save key to a non-existent directory.")

read_key = get_key('./testDir/.env')
print("Read Key from non-existent directory:", read_key)
if read_key == key:
    print("Key successfully saved and retrieved from non-existent directory.")
else:
    print("Error: The saved key does not match the generated key from non-existent directory.")
print("Key generation and retrieval test with non existent directory completed.")
