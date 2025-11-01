import sys
from PyQt6.QtWidgets import QApplication
from src.gui import NotionDiscordGUI
from src.live_reload import start_live_reload

if __name__ == '__main__':
    # Start live reload for development
    start_live_reload()

    app = QApplication(sys.argv)
    try:
        # Load client_id from config, will be set by setup dialog if needed
        try:
            import json
            with open('config.json', 'r') as f:
                config = json.load(f)
            client_id = config.get('client_id', '')
        except:
            client_id = ''
        window = NotionDiscordGUI(client_id)
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error starting app: {e}")
        import traceback
        traceback.print_exc()
