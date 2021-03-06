from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import ContentImage
from blog.forms import CommentForm, ReplyForm
from blog.models import Post, Category, Tag, Comment, Reply, New, Novel, Chapter, Story
from django.shortcuts import render

class LaterView(TemplateView):
    template_name = 'blog/later.html'


class NovelView(TemplateView):
    template_name = 'blog/novel.html'

    def get(self, request, *args, **kwargs):
        context = {
            'novel_list': Novel.objects.all(),
        }
        return self.render_to_response(context)


class ChapterView(TemplateView):
    template_name = 'blog/chapter.html'

    def get(self, request, *args, **kwargs):
        novel_pk = self.kwargs['novel_pk']
        context = {
            'novel_pk': novel_pk,
            'chapter_list': Chapter.objects.filter(novel_id=novel_pk),
        }
        return self.render_to_response(context)


class StoryView(TemplateView):
    template_name = 'blog/story.html'

    def get(self, request, *args, **kwargs):
        novel_pk = self.kwargs['novel_pk']
        chapter_pk = self.kwargs['chapter_pk']
        context = {
            'novel_pk': novel_pk,
            'chapter_pk': chapter_pk,
            'story_list': Story.objects.filter(chapter_id=chapter_pk),
        }
        return self.render_to_response(context)


class Story_DetailView(TemplateView):
    template_name = 'blog/story_detail.html'

    def get(self, request, *args, **kwargs):
        story_pk = self.kwargs['story_pk']
        context = {
            'story_pk': story_pk,
            'story_list': Story.objects.filter(id=story_pk),
        }
        return self.render_to_response(context)


class MemberView(TemplateView):
    template_name = 'blog/member.html'

class NewsView(TemplateView):
    template_name = 'blog/news.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        context = {
            'news_list': New.objects.all().order_by('-created_at')
        }
        return self.render_to_response(context)

def get_pic(request):
    images = ContentImage.objects.all().order_by('-created_at')
    return render(request, 'blog/post_detail.html', {'images': images})


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context['post'])
        context['image'] = ContentImage.objects.filter(post=context['post'])
        print(context['image'])
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        return obj


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 3

class CategoryPostView(ListView):
    model = Post
    template_name = 'blog/category_post.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagPostView(ListView):
    model = Post
    template_name = 'blog/tag_post.html'

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        qs = super().get_queryset().filter(tags=self.tag)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class SearchPostView(ListView):
    model = Post
    template_name = 'blog/search_post.html'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(category__name__icontains=query) |
                Q(tags__name__icontains=query)
        )
        if query is not None:
            qs = super().get_queryset().filter(lookups).distinct()
            return qs
        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context


class CategoryListView(ListView):
    queryset = Category.objects.annotate(
        num_posts=Count('post', filter=Q(post__is_public=True)))


class TagListView(ListView):
    queryset = Tag.objects.annotate(num_posts=Count(
        'post', filter=Q(post__is_public=True)))


class CommentFormView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        post_pk = self.kwargs['pk']
        comment.post = get_object_or_404(Post, pk=post_pk)
        comment.save()
        return redirect('blog:post_detail', pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['pk']
        context['post'] = get_object_or_404(Post, pk=post_pk)
        return context


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog:post_detail', pk=comment.post.pk)


class ReplyFormView(CreateView):
    model = Reply
    form_class = ReplyForm

    def form_valid(self, form):
        reply = form.save(commit=False)
        comment_pk = self.kwargs['pk']
        reply.comment = get_object_or_404(Comment, pk=comment_pk)
        reply.save()
        return redirect('blog:post_detail', pk=reply.comment.post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['pk']
        context['comment'] = get_object_or_404(Comment, pk=comment_pk)
        return context


@login_required
def reply_approve(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    reply.approve()
    return redirect('blog:post_detail', pk=reply.comment.post.pk)


@login_required
def reply_remove(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    reply.delete()
    return redirect('blog:post_detail', pk=reply.comment.post.pk)
