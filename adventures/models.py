from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.

STATUS = ((0, "Draft"), (1, "Published"))


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="blog_posts")
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    excerpt = models.TextField(blank=True)

    tags = models.ManyToManyField('Tag', through='PostTag', related_name='posts')

    class meta:
            ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title}| Written by {self.author}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='commenter', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  

    class meta:
        ordering = ["created_at"]
    def __str__(self):
        return f"Comment by {self.content} by {self.user}"


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True) 
    tag_type = models.CharField(max_length=50, unique=True)  #tag type should be hiking, location, advert,  
    description = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag_type

class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Optional field for tracking when the relationship was added

    class Meta:
        unique_together = ('post', 'tag')  # Composite primary key ensuring unique post-tag pairs
        verbose_name = 'Post Tag'  # For display purposes in admin, optional
        verbose_name_plural = 'Post Tags'

    def __str__(self):
        return f"{self.post.title} - {self.tag.name}"


