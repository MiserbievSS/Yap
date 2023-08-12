from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    color = models.CharField(max_length=7)
    slug = models.SlugField(max_length=200)
    name = models.CharField(max_length=200, unique=True)


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, related_name='recipes')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes/')
    text = models.TextField()
    cooking_time = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True,)

    class Meta:
        ordering = ('-pub_date',)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()


class FavoriteList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_favorited'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_favorited'
    )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_in_shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_in_shopping_cart'
    )
