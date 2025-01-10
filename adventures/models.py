from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.

STATUS = ((0, "Draft"), (1, "Published"))


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    
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
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, blank=True, null=True)
    activity = models.CharField(max_length=20, choices=ACTIVITIES_CHOICES, blank=True, null=True)
    type_choices = models.CharField(max_length=20, choices=TYPE_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"Location: {self.location or 'N/A'}, Activity: {self.activity or 'N/A'}, Type: {self.type_choices or 'N/A'}"


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="blog_posts")
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    excerpt = models.TextField(blank=True)

    tags = models.ManyToManyField(Tag, through='PostTag', related_name='posts')

    class Meta:
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

    class Meta:
        ordering = ["created_at"]
    def __str__(self):
        return f"Comment by {self.content} by {self.user}"


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'tag')  # Composite primary key ensuring unique post-tag pairs

    def __str__(self):
        return f"{self.post.title} - {self.tag.location or self.tag.activity or self.tag.type}"



class About(models.Model):
    title = models.CharField(max_length=200)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return self.title


class CollaborateRequest(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Collaboration request from {self.name}"