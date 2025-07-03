import os
from Crypto.Random import get_random_bytes

def secure_delete(file_path):
    """Securely delete a file by overwriting it with random data three times."""
    try:
        # Determine the file size
        with open(file_path, 'ba+') as f:
            length = f.tell()
        
        # Overwrite the file three times with random data
        for _ in range(3):
            with open(file_path, 'br+') as f:
                f.seek(0)
                f.write(get_random_bytes(length))

        # Physically remove the file from disk
        os.remove(file_path)

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except Exception as e:
        raise Exception(f"Secure deletion failed: {e}")
