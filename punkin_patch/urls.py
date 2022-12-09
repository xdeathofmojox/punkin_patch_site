from django.urls import path
from .characterViews import CharacterList, CharacterDetail, CharacterCreate, CharacterUpdate, CharacterDelete

urlpatterns = [
    path('characters/', CharacterList.as_view(), name='characters'),
    path('character/<int:pk>/', CharacterDetail.as_view(), name='character'),
    path('character-create/', CharacterCreate.as_view(), name='character-create'),
    path('character-update/<int:pk>/', CharacterUpdate.as_view(), name='character-update'),
    path('character-delete/<int:pk>/', CharacterDelete.as_view(), name='character-delete'),
]