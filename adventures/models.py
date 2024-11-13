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
    # category choices defined
    LOCATION = 'location'
    ACTIVITIES = 'activities'
    TYPE_OF_POST = 'type_of_post'
    #Lists that provide the actual choices 
    CATEGORY_CHOICES = [
        (LOCATION, 'Location'),
        (ACTIVITIES, 'Activities'),
        (TYPE_OF_POST, 'Type of Post'),
    ]

    #tag options for each category
    LOCATION_CHOICES = [
        ('europe', 'Europe'),
        ('asia', 'Asia'),
        ('africa', 'Africa'),
        ('north_america', 'North America'),
        ('south_america', 'South America'),
        ('australia', 'Australia'),
        ('antarctica', 'Antarctica'),
    ]

    ACTIVITIES_CHOICES = [
        ('hiking', 'Hiking'),
        ('camping', 'Camping'),
        ('fishing', 'Fishing'),
        ('skiing', 'Skiing'),
        ('snowboarding', 'Snowboarding'),
        ('sailing', 'Sailing'),
        ('kitesurfing', 'Kite Surfing'),
        ('surfing', 'Surfing'),
        ('mountainbiking', 'Mountain Biking'),
        ('foiling', 'foiling'),
        ('cycling', 'Cycling'),
        ('running', 'Running'),
    ]

    TYPE_CHOICES = [
        ('promo', 'Promo'),
        ('blog', 'Blog'),
    ]

    # Fields for category and tag ID
    tag_id = models.AutoField(primary_key=True) 
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    

    def __str__(self):
        return f"{self.get_category_display()}: {self.category}"

class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'tag')  # Composite primary key ensuring unique post-tag pairs
        post_tag_combo = 'Post Tag'  

    def __str__(self):
        return f"{self.post.title} - {self.tag.name}"


