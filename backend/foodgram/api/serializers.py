from rest_framework.exceptions import ValidationError
from django.db.models import F
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import status
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from api.validators import (
    validate_ingredients,
    validate_tags,
    validate_cooking_time)
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.models import Subscription, User


class SubscribeRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'first_name', 'last_name',)
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscription.objects.filter(
                user=user, author=obj.id
            ).exists()
        return False


class SubscriptionSerializer(UserSerializer):
    id = serializers.IntegerField(source='author.id')
    first_name = serializers.CharField(source='author.first_name')
    last_name = serializers.CharField(source='author.last_name')
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subscription
        fields = (
            'id',
            'first_name',
            'last_name',
            'recipes',
            'recipes_count',
        )

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if Subscription.objects.filter(author=author, user=user).exists():
            raise ValidationError(
                detail='Вы уже подписаны на этого пользователя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise ValidationError(
                detail='Вы не можете подписаться на самого себя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data

    def get_recipes(self, obj):
        recipes_limit = self.context.get('request').GET.get('recipes_limit')
        recipes = obj.author.recipes.all()
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        serializer = SubscribeRecipeSerializer(recipes, many=True)

        return serializer.data

    def get_recipes_count(self, obj):
        return obj.author.recipes.all().count()


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tags = TagSerializer(read_only=True, many=True)
    image = Base64ImageField()
    ingredients = SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags',
                  'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image',
                  'text', 'cooking_time',)

    def get_ingredients(self, obj):
        return obj.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipeingredient__amount')
        )

    def get_is_favorited(self, obj):
        user_id = self.context.get('request').user.id
        return obj.is_favorited.filter(user_id=user_id).exists()

    def get_is_in_shopping_cart(self, obj):
        user_id = self.context.get('request').user.id
        return obj.is_in_shopping_cart.filter(user_id=user_id).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = RecipeIngredientSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'name',
            'author',
            'image',
            'cooking_time',
            'text',
            'tags',
            'ingredients'
        )
    
    def validate(self, data):
        validate_tags(self.initial_data.get('tags')),
        validate_ingredients(
            self.initial_data.get('ingredients')
        )
        validate_cooking_time(
            self.initial_data.get('cooking_time')
        )
        return data
    # def validate_tags(self, tags):
    #     if not tags:
    #         raise serializers.ValidationError(
    #             'Выберите тег'
    #         )
    #     return tags

    # def validate_ingredients(self, ingredients):
    #     if not ingredients:
    #         raise serializers.ValidationError({
    #             'ingredients': 'Выберите хотя бы один ингредиент!'
    #         })
    #     ingredients_list = []
    #     for item in ingredients:
    #         ingredient = get_object_or_404(Ingredient, id=item['id'])
    #         if ingredient in ingredients_list:
    #             raise serializers.ValidationError({
    #                 'ingredients': 'Ингредиенты не должны повторяться!'
    #             })
    #         if int(item['amount']) <= 0:
    #             raise serializers.ValidationError({
    #                 'amount': 'Количество ингредиента должно быть больше 0'
    #             })
    #         ingredients_list.append(ingredient)
    #     return ingredients

    def add_tags_and_ingredients(self, tags, ingredients, recipe):
        recipe.tags.set(tags)
        recipe_ingredients = []
        for ingredient in ingredients:
            recipe_ingredients.append(RecipeIngredient(
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
                recipe=recipe
            ))

        return RecipeIngredient.objects.bulk_create(recipe_ingredients)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.add_tags_and_ingredients(tags, ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        name = validated_data.pop('name')
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        text = validated_data.pop('text')
        cooking_time = validated_data.pop('cooking_time')
        instance.ingredients.clear()
        self.add_tags_and_ingredients(tags, ingredients_data, instance)

        instance.tags.set(tags)
        instance.name = name
        instance.text = text
        instance.cooking_time = cooking_time

        instance.save()
        return instance
