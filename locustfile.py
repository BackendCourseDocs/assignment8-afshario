from locust import HttpUser, task

class QuickstartUser(HttpUser):    
    @task
    def search_book(self):
        self.client.get("/books/?q=all&page=1&size=1")