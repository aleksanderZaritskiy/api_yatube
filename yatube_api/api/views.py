from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from posts.models import Post, Group, Comment
from .permissions import OnlyAuthorHasPerm
from .serializers import (
    PostSerializer, GroupSerializer,
    CommentSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (OnlyAuthorHasPerm,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (OnlyAuthorHasPerm,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
