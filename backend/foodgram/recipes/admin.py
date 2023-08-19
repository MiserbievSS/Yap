from django.contrib import admin

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
    list_display = ('pk', 'name', 'author', 'get_favourited',
                    'get_tags', 'created')
    list_filter = ('author', 'tags')
    search_fields = ('name', 'author__username', 'ingredients__name')

    def get_favourited(self, obj):
        return obj.favourites.count()

    get_favourited.short_description = 'Рецепт добавлен в избранное'

    def get_tags(self, obj):
        return '\n'.join(obj.tags.values_list('name', flat=True))

    get_tags.short_description = 'Тэг или список тэгов'

    def get_ingredients(self, obj):
        return '\n'.join(obj.ingredients.values_list('name', flat=True))

    get_ingredients.short_description = 'Ингредиент или список ингредиентов'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(FavoriteList)
class FavoriteListAdmin(admin.ModelAdmin):
    pass


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    pass
