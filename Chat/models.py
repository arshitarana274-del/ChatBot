from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.role}: {self.content[:20]}"