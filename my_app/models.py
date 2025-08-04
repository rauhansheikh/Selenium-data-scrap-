from django.db import models

class SearchResult(models.Model):
    query = models.CharField(max_length=255)
    title = models.TextField()
    link = models.URLField()
    snippet = models.TextField(blank=True)  # ✅ add this line
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
