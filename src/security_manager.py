"""
Security Manager - Handles AES encryption/decryption for sensitive config data
Uses triple AES encryption (3 times) for enhanced security
"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import json


class SecurityManager:
    """Manages encryption and decryption of sensitive configuration data"""
    
    # Fixed salt for consistent key derivation (in production, consider per-user salt)
    SALT = b'NotionPresence_Security_Salt_2025'
    ENCRYPTION_ROUNDS = 3
    
    @staticmethod
    def _derive_key(password: str) -> bytes:
        """Derive encryption key from password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=SecurityManager.SALT,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    @staticmethod
    def _get_encryption_key() -> bytes:
        """Get the encryption key (derived from machine identifier)"""
        # Use machine name and username for key derivation
        machine_id = f"{os.getenv('COMPUTERNAME')}_{os.getenv('USERNAME')}"
        return SecurityManager._derive_key(machine_id)
    
    @staticmethod
    def encrypt_value(value: str) -> str:
        """
        Encrypt a value using triple AES encryption
        
        Args:
            value: String value to encrypt
            
        Returns:
            Triple-encrypted base64 string
        """
        try:
            key = SecurityManager._get_encryption_key()
            encrypted = value
            
            # Apply encryption 3 times
            for i in range(SecurityManager.ENCRYPTION_ROUNDS):
                cipher = Fernet(key)
                encrypted = cipher.encrypt(encrypted.encode()).decode()
            
            return encrypted
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")
    
    @staticmethod
    def decrypt_value(encrypted_value: str) -> str:
        """
        Decrypt a value using triple AES decryption (reverse order)
        
        Args:
            encrypted_value: Triple-encrypted base64 string
            
        Returns:
            Decrypted original value
        """
        try:
            key = SecurityManager._get_encryption_key()
            decrypted = encrypted_value
            
            # Apply decryption 3 times (reverse order)
            for i in range(SecurityManager.ENCRYPTION_ROUNDS):
                cipher = Fernet(key)
                decrypted = cipher.decrypt(decrypted.encode()).decode()
            
            return decrypted
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")
    
    @staticmethod
    def encrypt_config(config: dict) -> dict:
        """
        Encrypt sensitive fields in config
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Config with encrypted sensitive fields
        """
        encrypted_config = config.copy()
        
        # Encrypt sensitive fields
        sensitive_fields = ['notion_token', 'client_id']
        
        for field in sensitive_fields:
            if field in encrypted_config and encrypted_config[field]:
                encrypted_config[field] = SecurityManager.encrypt_value(encrypted_config[field])
        
        return encrypted_config
    
    @staticmethod
    def decrypt_config(encrypted_config: dict) -> dict:
        """
        Decrypt sensitive fields in config
        
        Args:
            encrypted_config: Configuration dictionary with encrypted fields
            
        Returns:
            Config with decrypted sensitive fields
        """
        decrypted_config = encrypted_config.copy()
        
        # Decrypt sensitive fields
        sensitive_fields = ['notion_token', 'client_id']
        
        for field in sensitive_fields:
            if field in decrypted_config and decrypted_config[field]:
                try:
                    decrypted_config[field] = SecurityManager.decrypt_value(decrypted_config[field])
                except Exception as e:
                    # If decryption fails, return original (might be unencrypted)
                    pass
        
        return decrypted_config
    
    @staticmethod
    def save_encrypted_config(config: dict, filepath: str) -> bool:
        """
        Save config with encrypted sensitive fields
        
        Args:
            config: Configuration dictionary
            filepath: Path to save config file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            encrypted_config = SecurityManager.encrypt_config(config)
            with open(filepath, 'w') as f:
                json.dump(encrypted_config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving encrypted config: {str(e)}")
            return False
    
    @staticmethod
    def load_encrypted_config(filepath: str) -> dict:
        """
        Load config and decrypt sensitive fields
        
        Args:
            filepath: Path to config file
            
        Returns:
            Decrypted configuration dictionary
        """
        try:
            # Check if file exists
            if not os.path.exists(filepath):
                # print(f"Config file not found: {filepath}. Creating new config...")
                return SecurityManager._create_default_config(filepath)
            
            # Check if file is empty
            if os.path.getsize(filepath) == 0:
                # print(f"Config file is empty. Creating new config...")
                return SecurityManager._create_default_config(filepath)
            
            with open(filepath, 'r') as f:
                content = f.read().strip()
                
                # Check if content is empty after stripping
                if not content:
                    # print(f"Config file is empty. Creating new config...")
                    return SecurityManager._create_default_config(filepath)
                
                encrypted_config = json.loads(content)
            
            decrypted_config = SecurityManager.decrypt_config(encrypted_config)
            return decrypted_config
        except json.JSONDecodeError as e:
            # print(f"Config file is corrupted (JSON error): {str(e)}. Creating new config...")
            return SecurityManager._create_default_config(filepath)
        except Exception as e:
            # print(f"Error loading encrypted config: {str(e)}. Creating new config...")
            return SecurityManager._create_default_config(filepath)
    
    @staticmethod
    def _create_default_config(filepath: str) -> dict:
        """
        Create a default empty config file
        
        Args:
            filepath: Path to config file
            
        Returns:
            Default configuration dictionary
        """
        default_config = {
            "notion_token": "",
            "id": "",
            "client_id": ""
        }
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
            
            # Save default config
            with open(filepath, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            # print(f"Created new config file: {filepath}")
        except Exception as e:
            # print(f"Error creating default config: {str(e)}")
            pass
        
        return default_config
    
    @staticmethod
    def is_encrypted(value: str) -> bool:
        """
        Check if a value appears to be encrypted (Fernet format)
        
        Args:
            value: Value to check
            
        Returns:
            True if value appears encrypted, False otherwise
        """
        if not value:
            return False
        try:
            # Fernet tokens start with 'gAAAAAA'
            return value.startswith('gAAAAAA')
        except:
            return False
