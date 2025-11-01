from PyQt6.QtCore import QTimer
from ..discord_presence import DiscordPresence
from ..notion_api import NotionAPI
import psutil
import json

class PresenceManager:
    def __init__(self, gui, client_id):
        self.gui = gui
        self.discord_presence = DiscordPresence(client_id)

    def connect_discord_thread(self):
        try:
            self.discord_presence.connect()
            self.update_status(True, "Connected to Discord")
        except Exception as e:
            self.update_status(False, f"Failed to connect: {str(e)}")

    def update_status(self, success, message):
        if success:
            self.gui.status_label.setText("Status: Connected to Discord")
            self.gui.status_label.setStyleSheet("#statusLabel { margin: 0px; padding: 0px; font-weight: bold; font-size: 12px; color: #57f287; }")
        else:
            self.gui.status_label.setText(f"Status: {message}")
            self.gui.status_label.setStyleSheet("#statusLabel { margin: 0px; padding: 0px; font-weight: bold; font-size: 12px; color: #ed4245; }")

    def auto_update_presence(self):
        if self.gui.config.get('id'):
            try:
                api = NotionAPI(self.gui.config['notion_token'])
                title, _ = api.get_page_title_and_parent(self.gui.config['id'])
                if title:
                    # Enhanced presence with details and state
                    self.discord_presence.update_presence(
                        details=f"📝 {title}",
                        state="Working on Notion",
                        large_text="Notion Discord Auto RPC",
                        large_image="notion",
                        small_text="Active",
                        small_image="active"
                    )
                    self.gui.presence_label.setText(f"Presence: {title}")
                else:
                    self.discord_presence.update_presence(
                        details="Using Notion",
                        state="Browsing",
                        large_text="Notion Discord Auto RPC",
                        large_image="notion"
                    )
                    self.gui.presence_label.setText("Presence: Using Notion")
            except Exception as e:
                self.discord_presence.update_presence(
                    details="Using Notion",
                    state="Browsing",
                    large_text="Notion Discord Auto RPC",
                    large_image="notion"
                )
                self.gui.presence_label.setText("Presence: Using Notion")
        else:
            self.discord_presence.update_presence(
                details="Using Notion",
                state="Browsing",
                large_text="Notion Discord Auto RPC",
                large_image="notion"
            )
            self.gui.presence_label.setText("Presence: Using Notion")

    def clear_presence(self):
        self.discord_presence.clear_presence()
        self.gui.presence_label.setText("Presence: Cleared")
        # Clear the selected page to prevent auto-update from re-setting presence
        self.gui.config['id'] = ""
        try:
            with open('config.json', 'w') as f:
                json.dump(self.gui.config, f)
        except:
            pass
