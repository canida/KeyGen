from cryptography.fernet import Fernet
from dotenv import dotenv_values
import os
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Get file paths from config
key_file = config.get('paths', 'key_file', fallback='.env')



def generate_key():
    """
    Generate a new Fernet key.
    
    Returns:
        str: A base64 encoded key as a string.
    """
    return Fernet.generate_key().decode('utf-8')


def get_key(filename):
    """
    Retrieve the key from a file.
    
    Args:
        filename (str): The file path where the key is stored.
        
    Returns:
        str: The key read from the file.
    """
   
    
    with open(filename, 'rb') as file:
        return file.read().decode('utf-8')

def save_key_to_file(key, filename=key_file):
    """
    Save the provided key to a file.
    
    Args:
        key (str): The key to save.
        filename (str): The file path where the key will be saved.
    """
    if  not os.path.exists(os.path.dirname(filename)):
        # Create the directory if it does not exist and it is the default key file
        if key_file == filename:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as file:
        file.write(key.encode('utf-8'))


key = generate_key()
print("Generated Key:", key)
file = os.path.dirname(__file__) + "/.env"
print("File:", file)
save_key_to_file(key,file)

print("Key_file:", key_file)
