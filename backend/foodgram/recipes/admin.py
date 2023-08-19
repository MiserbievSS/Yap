from django.contrib import admin
from django.contrib.admin import display

from recipes.models import (FavoriteList, Ingredient, Recipe,
                            ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_filter = ('author', 'name', 'tags',)
    list_display = ('name', 'id', 'author', 'added_in_favorited')
    filter_horizontal = ('ingredients',)

    def get_tags(self, obj):
        return '\n'.join(obj.tags.values_list('name', flat=True))

    get_tags.short_description = 'Тэг или список тэгов'

    def get_ingredients(self, obj):
        return '\n'.join(obj.ingredients.values_list('name', flat=True))

    get_ingredients.short_description = 'Ингредиент или список ингредиентов'

    @display(description='количество в избранных')
    def added_in_favorited(self, obj):
        return obj.is_favorited.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


@admin.register(FavoriteList)
class FavoriteListAdmin(admin.ModelAdmin):
    pass


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    pass
