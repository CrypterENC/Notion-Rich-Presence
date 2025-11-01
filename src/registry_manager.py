"""
Windows Registry Manager - Handles app registration and startup configuration
"""

import winreg
import os
import sys


class RegistryManager:
    """Manages Windows registry entries for app startup and registration"""
    
    REGISTRY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
    APP_NAME = "NotionPresence"
    
    @staticmethod
    def get_app_path():
        """Get the path to the main executable"""
        if getattr(sys, 'frozen', False):
            # If running as compiled exe
            return sys.executable
        else:
            # If running as script
            return os.path.join(os.path.dirname(__file__), '..', 'main.py')
    
    @staticmethod
    def register_startup():
        """Register app to run on Windows startup"""
        try:
            app_path = RegistryManager.get_app_path()
            
            # Open registry key with write access
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                RegistryManager.REGISTRY_PATH,
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Set registry value - without quotes for proper execution
            winreg.SetValueEx(
                key,
                RegistryManager.APP_NAME,
                0,
                winreg.REG_SZ,
                app_path
            )
            
            winreg.CloseKey(key)
            return True, "App registered for startup successfully"
        except PermissionError:
            return False, "Permission denied: Run as Administrator to register startup"
        except Exception as e:
            return False, f"Error registering startup: {str(e)}"
    
    @staticmethod
    def unregister_startup():
        """Remove app from Windows startup"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                RegistryManager.REGISTRY_PATH,
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Delete registry value
            winreg.DeleteValue(key, RegistryManager.APP_NAME)
            winreg.CloseKey(key)
            return True, "App removed from startup successfully"
        except FileNotFoundError:
            return False, "App not found in startup registry"
        except PermissionError:
            return False, "Permission denied: Run as Administrator to unregister"
        except Exception as e:
            return False, f"Error unregistering startup: {str(e)}"
    
    @staticmethod
    def is_registered():
        """Check if app is registered for startup"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                RegistryManager.REGISTRY_PATH,
                0,
                winreg.KEY_READ
            )
            
            try:
                winreg.QueryValueEx(key, RegistryManager.APP_NAME)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception:
            return False
    
    @staticmethod
    def create_app_registry_entries():
        """Create additional app registry entries for proper Windows integration"""
        try:
            app_path = RegistryManager.get_app_path()
            app_name = RegistryManager.APP_NAME
            
            # Create app entry in Uninstall registry (for Add/Remove Programs)
            uninstall_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
            
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{uninstall_path}\\{app_name}")
            
            winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, "Notion Discord Auto RPC")
            winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, "1.0.0")
            winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, "CrypterENC")
            winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, app_path)
            
            winreg.CloseKey(key)
            return True, "App registry entries created successfully"
        except PermissionError:
            return False, "Permission denied: Run as Administrator"
        except Exception as e:
            return False, f"Error creating registry entries: {str(e)}"
