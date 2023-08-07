from rest_framework import routers
from django.urls import include, path

from api.views import CustomUserViewSet, TagViewSet, RecipeViewSet, IngredientViewSet

router = routers.DefaultRouter()
router.register('users', CustomUserViewSet)
router.register('tags', TagViewSet)
router.register('ingredient', IngredientViewSet)
router.register('recipes', RecipeViewSet)


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
