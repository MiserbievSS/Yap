from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .pagination import LimitPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, SubscribeRecipeSerializer,
                          SubscriptionSerializer, TagSerializer)
from recipes.models import (FavoriteList, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Subscription, User


class UserViewSet(UserViewSet):
    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = request.user
        queryset = Subscription.objects.filter(user=user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            page, many=True, context={'request': request}
        )

        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                Subscription.objects.create(user=request.user, author=author),
                context={'request': request},
            )
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            Subscription.objects.filter(
                user=request.user, author=author
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filterset_class = IngredientFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitPageNumberPagination
    filterset_class = RecipeFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action == 'create':
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def operations_shopping_and_favorite_cart(self, request, id, model):
        if request.method == 'POST':
            if model.objects.filter(user=request.user, recipe__id=id):
                return Response({'error': 'Рецепт уже находится в корзине'})
            recipe = get_object_or_404(Recipe, id=id)
            model.objects.create(user=request.user, recipe=recipe)
            serializer = SubscribeRecipeSerializer(recipe)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        cart = model.objects.filter(user=request.user, recipe__id=id)
        if not cart.exists():
            return Response({'error': 'Рецепт уже удалён из корзины'})
        cart.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        return self.operations_shopping_and_favorite_cart(
            request,
            pk,
            FavoriteList
        )

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        return self.operations_shopping_and_favorite_cart(
            request,
            pk,
            ShoppingCart
        )

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = request.user
        recipes = ShoppingCart.objects.filter(user=user)
        file_name = 'shopping_cart.txt'
        with open(file_name, 'w') as file:
            for recipe in recipes:
                recipe = recipe.recipe
                recipe_string = f'Рецепт: {recipe.name}\nИнгредиенты:\n'
                ingredients = RecipeIngredient.objects.filter(recipe=recipe.id)
                for ingredient in ingredients:
                    amount = ingredient.amount
                    ingredient = Ingredient.objects.get(
                        pk=ingredient.ingredient.id
                    )
                    recipe_string += str(
                        f'{ingredient.name} - {amount} '
                        + f'{ingredient.measurement_unit}'
                    )
                file.write(recipe_string)
        return FileResponse(open(file_name, 'rb'), as_attachment=True)
