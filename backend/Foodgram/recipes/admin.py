from django.contrib import admin

from recipes.models import Tag, Recipe, Ingredient, RecipeIngredient, FavoriteList, ShoppingCart


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass

@admin.register(FavoriteList)
class FavoriteListAdmin(admin.ModelAdmin):
    pass

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    pass