import requests

class NotionAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json'
        }

    def get_recent_pages(self, database_id, limit=1):
        url = f'https://api.notion.com/v1/databases/{database_id}/query'
        data = {
            "sorts": [
                {
                    "timestamp": "last_edited_time",
                    "direction": "descending"
                }
            ],
            "page_size": limit
        }
        try:
            response = requests.post(url, headers=self.headers, json=data)
            # print(f"API Response Status: {response.status_code}")
            if response.status_code == 200:
                results = response.json().get('results', [])
                if results:
                    page = results[0]
                    title = self.get_title(page)
                    return title
                else:
                    # print("No pages found in database")
                    return None
            elif response.status_code == 404 or (response.status_code == 400 and 'page' in response.text.lower()):
                # print("Not a database, trying as page...")
                title, _ = self.get_page_title_and_parent(database_id)
                return title
            else:
                # print(f"API Error: {response.text}")
                return None
        except Exception as e:
            # print(f"Notion API Exception: {e}")
            return None

    def get_page_title_and_parent(self, page_id):
        url = f'https://api.notion.com/v1/pages/{page_id}'
        try:
            response = requests.get(url, headers=self.headers)
            # print(f"Page API Response Status: {response.status_code}")
            if response.status_code == 200:
                page = response.json()
                title = self.get_title(page)
                parent = page.get('parent', {})
                parent_id = parent.get('page_id') or parent.get('database_id')
                return title, parent_id
            else:
                # print(f"Page API Error: {response.text}")
                return None, None
        except Exception as e:
            # print(f"Page API Exception: {e}")
            return None, None

    def get_all_page_ids(self):
        url = 'https://api.notion.com/v1/search'
        page_ids = []
        start_cursor = None
        while True:
            data = {
                "query": "",
                "filter": {"property": "object", "value": "page"},
                "page_size": 100  # Max 100 per request
            }
            if start_cursor:
                data["start_cursor"] = start_cursor
            try:
                response = requests.post(url, headers=self.headers, json=data)
                # print(f"Search API Response Status: {response.status_code}")
                if response.status_code == 200:
                    json_response = response.json()
                    results = json_response.get('results', [])
                    page_ids.extend([item['id'] for item in results if item.get('object') == 'page'])
                    has_more = json_response.get('has_more', False)
                    if not has_more:
                        break
                    start_cursor = json_response.get('next_cursor')
                else:
                    # print(f"Search API Error: {response.text}")
                    break
            except Exception as e:
                # print(f"Search API Exception: {e}")
                break
        return page_ids

    def get_title(self, page):
        properties = page.get('properties', {})
        for prop in properties.values():
            if prop.get('type') == 'title':
                title_texts = prop.get('title', [])
                if title_texts:
                    return ''.join([t.get('plain_text', '') for t in title_texts])
        return 'Untitled'
