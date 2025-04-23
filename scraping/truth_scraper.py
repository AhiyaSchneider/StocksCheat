from truthbrush.api import Api

class TruthScraper:
    def __init__(self, username, password):
        self.client = Api()
        self.username = username
        self.password = password
        self.authenticate()

    def authenticate(self):
        # Implement authentication logic if required
        pass

    def fetch_posts(self, user_handle, limit=1):
        posts = self.client.pull_statuses(username=user_handle, replies=False, pinned=False)
        posts_list = list(posts)

        # Map each post to the expected structure
        formatted_posts = []
        for post in posts_list[:limit]:
            formatted_posts.append({
                'post_date': post['created_at'],
                'content': post['content'],
                'user_handle': user_handle,
                'source': 'truthsocial',
                'stock_related': False,
                'stock_name': 'N/A',
                'influence': None
            })

        return formatted_posts
