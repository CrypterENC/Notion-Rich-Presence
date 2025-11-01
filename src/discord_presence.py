from pypresence import Presence
import time

class DiscordPresence:
    def __init__(self, client_id):
        self.client_id = client_id
        self.rpc = None
        self.connected = False
        self.start_time = None

    def connect(self):
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            self.connected = True
            self.start_time = int(time.time())
            return True, "Connected to Discord"
        except Exception as e:
            self.connected = False
            return False, f"Failed to connect: {str(e)}"

    def update_presence(self, details=None, state=None, large_text=None, small_text=None, large_image=None, small_image=None):
        if not self.connected or not self.rpc:
            return False, "Not connected to Discord"
        try:
            # Build presence update with enhanced fields
            presence_data = {
                'details': details,
                'state': state,
                'start': self.start_time,
                'large_text': large_text or 'Notion Discord Auto RPC',
                'large_image': large_image or 'notion',
            }
            
            # Add optional fields if provided
            if small_text:
                presence_data['small_text'] = small_text
            if small_image:
                presence_data['small_image'] = small_image
            
            self.rpc.update(**presence_data)
            return True, "Presence updated"
        except Exception as e:
            return False, f"Error updating presence: {str(e)}"

    def clear_presence(self):
        if not self.connected or not self.rpc:
            return False, "Not connected to Discord"
        try:
            self.rpc.clear()
            self.start_time = None
            return True, "Presence cleared"
        except Exception as e:
            return False, f"Error clearing presence: {str(e)}"
