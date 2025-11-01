import concurrent.futures
from PyQt6.QtWidgets import QMessageBox, QLabel, QComboBox
from ..notion_api import NotionAPI

class PageManager:
    def __init__(self, gui):
        self.gui = gui

    def reload_pages(self):
        try:
            self.gui.pages = []
            if self.gui.config.get('notion_token'):
                api = NotionAPI(self.gui.config['notion_token'])
                page_ids = api.get_all_page_ids()
                if page_ids:
                    page_ids_limited = page_ids  # Process all pages
                    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                        results = list(executor.map(api.get_page_title_and_parent, page_ids_limited))
                    # Build hierarchy
                    children = {}
                    roots = []
                    for pid, (title, parent_id) in zip(page_ids_limited, results):
                        if title:
                            if parent_id:
                                if parent_id not in children:
                                    children[parent_id] = []
                                children[parent_id].append((pid, title))
                            else:
                                roots.append((pid, title))
                    # Flatten with indentation
                    def flatten_hierarchy(items, indent=0):
                        result = []
                        for pid, title in sorted(items, key=lambda x: x[1]):
                            result.append((pid, "  " * indent + title))
                            if pid in children:
                                result.extend(flatten_hierarchy(children[pid], indent + 1))
                        return result
                    self.gui.pages = flatten_hierarchy(roots)
                    # Debug print
                    # print("Hierarchical Pages:")
                    # for pid, title in self.gui.pages:
                    #     print(f"- {title} ({pid})")
            self.update_page_combo()
        except Exception as e:
            QMessageBox.critical(self.gui, "Error", f"Failed to load pages: {str(e)}")
            # print(f"Error loading pages: {e}")
            pass

    def update_page_combo(self):
        # Populate the combo box
        self.gui.page_combo.clear()
        if self.gui.pages:
            for pid, title in self.gui.pages:
                self.gui.page_combo.addItem(f"{title}", pid)
        else:
            self.gui.page_combo.addItem("No pages found", "")
