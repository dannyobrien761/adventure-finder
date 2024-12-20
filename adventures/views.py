from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post, PostTag, Tag
from django.core.paginator import Paginator

# Create your views here.

def post_list(request):
    """
    Displays a list of posts, optionally filtered by tags.
    """
    posts = Post.objects.filter(status=1).order_by('-created_on')

    # Filter posts by query parameters
    location = request.GET.get('location')
    activity = request.GET.get('activity')
    post_type = request.GET.get('type')

    if location:
        posts = posts.filter(tags__location=location)
    if activity:
        posts = posts.filter(tags__activity=activity)
    if post_type:
        posts = posts.filter(tags__type_choices=post_type)

    #queryset = queryset.distinct()  # Avoid duplicate posts if multiple tags overlap

    paginator = Paginator(posts, 6)  # Paginate with 6 posts per page
    page = request.GET.get('page')
    post_list = paginator.get_page(page)

    # Choices for filters
    location_choices = Tag.LOCATION_CHOICES
    activity_choices = Tag.ACTIVITIES_CHOICES
    type_choices = Tag.TYPE_CHOICES

    return render(
        request,
        "adventures/index.html",
        {
            "post_list": post_list,
            "current_filters": {"location": location, "activity": activity, "type": post_type},
            "location_choices": location_choices,
            "activity_choices": activity_choices,
            "type_choices": type_choices,
        },
    )


def post_detail(request, slug):
        """
        Display an individual :model:`blog.Post`.

        **Context**

        ``post``
            An instance of :model:`blog.Post`.

        **Template:**

        :template:`blog/post_detail.html`
        """

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)

        tags = PostTag.objects.filter(post=post).select_related('tag')

        return render(
        request,
        "adventures/post_detail.html",
        {"post": post, "tags": tags},
    )

