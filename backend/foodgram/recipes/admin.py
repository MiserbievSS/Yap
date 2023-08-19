from django.contrib import admin
from django.contrib.admin import display

from recipes.models import (FavoriteList, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_filter = ('author', 'name', 'tags', 'added_in_favorited')
    list_display = ('name', 'id', 'author', 'added_in_favorited')
    filter_horizontal = ('ingredients',)

    @display(description='количество в избранных')
    def added_in_favorited(self, obj):
        return obj.is_favorited.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(FavoriteList)
class FavoriteListAdmin(admin.ModelAdmin):
    pass


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    pass
