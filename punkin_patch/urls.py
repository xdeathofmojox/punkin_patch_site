from django.urls import path
from .characterViews import CharacterList, CharacterDetail, CharacterCreate, CharacterUpdate, CharacterDelete
from .patchViews import PatchList, PatchDetail, PatchCreate, PatchUpdate, PatchDelete

urlpatterns = [
    path('characters/', CharacterList.as_view(), name='characters'),
    path('character/<int:pk>/', CharacterDetail.as_view(), name='character'),
    path('character-create/', CharacterCreate.as_view(), name='character-create'),
    path('character-update/<int:pk>/', CharacterUpdate.as_view(), name='character-update'),
    path('character-delete/<int:pk>/', CharacterDelete.as_view(), name='character-delete'),
    path('patches/', PatchList.as_view(), name='patches'),
    path('patch/<int:pk>/', PatchDetail.as_view(), name='patch'),
    path('patch-create/', PatchCreate.as_view(), name='patch-create'),
    path('patch-update/<int:pk>/', PatchUpdate.as_view(), name='patch-update'),
    path('patch-delete/<int:pk>/', PatchDelete.as_view(), name='patch-delete'),
]