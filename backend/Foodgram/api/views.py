from django.shortcuts import HttpResponse
from djoser.views import UserViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet


from recipes.models import Tag, Recipe, Ingredient
from api.serializers import TagSerializer, RecipeSerializer, IngredientSerializer, RecipeCreateSerializer


class CustomUserViewSet(UserViewSet):
    pass

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_serializer_class(self):
        if self.action == 'create':    #сделать апдейт сериалайзера
            return RecipeCreateSerializer
        return RecipeSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    