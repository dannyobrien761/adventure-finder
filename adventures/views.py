from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from .models import Post, PostTag, Tag, Comment, Author
from django.core.paginator import Paginator
from .forms import CommentForm
from django.contrib import messages
from .models import About
from .forms import CollaborateForm
from django.http import HttpResponseRedirect

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

         # comments
        comments = post.comments.all().order_by("-created_at")
        comment_count = post.comments.filter(approved=True).count()

        if request.method == "POST": 
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                # Assign user and author
                comment.user = request.user  # Set the user field
                # Assign or create the Author instance for the user
                author, created = Author.objects.get_or_create(user=request.user)
                comment.author = author
                
                comment.post = post
                comment.save()
                messages.add_message(
                    request, messages.SUCCESS,
                    'Comment submitted and awaiting approval'
            )

        comment_form = CommentForm()

         #tags = PostTag.objects.filter(post=post).select_related('tag')

         # Get the tags associated with the current post
        tags = post.tags.all()  # This will get only the tags related to the current post
        print(tags) 
        # Now filter posts based on tagss, excluding the current post
        #related_posts = Post.objects.filter(tags__in=tags).exclude(id=post.id)[:4]

        related_posts = Post.objects.exclude(id=post.id)[:4]
        
        
        print(related_posts)  # Debugging: Check if related posts are being retrieved

        return render(
        request,
        "adventures/post_detail.html",
       {

            "post": post,
            "tags": tags,
            "related_posts": related_posts,
            "comments": comments,
            "comment_count": comment_count,
           "comment_form": comment_form,
        },
    )

def about_me(request):
    if request.method == "POST":
        collaborate_form = CollaborateForm(data=request.POST)
        if collaborate_form.is_valid():
            collaborate_form.save()
            messages.add_message(request, messages.SUCCESS, "Collaboration request received!")
    
    

    about = About.objects.all().order_by('-updated_on').first()
    collaborate_form = CollaborateForm()

    return render(
        request,
        "adventures/about.html",
        {
            "about": about,
            "collaborate_form": collaborate_form
        },
    )


def comment_edit(request, slug, comment_id):
    """
    View to edit comments. Allows both authors and regular users to edit their own comments.
    """
    if request.method == "POST":
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)

        # Ensure the user is the comment owner
        if comment.user != request.user:
            messages.add_message(request, messages.ERROR, "You are not authorized to edit this comment.")
            return HttpResponseRedirect(reverse('post_detail', args=[slug]))

        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False  # Reset approval status after edit
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment updated successfully and is pending approval.')
        else:
            messages.add_message(request, messages.ERROR, 'Failed to update the comment. Please check the form.')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))



def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.user == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))