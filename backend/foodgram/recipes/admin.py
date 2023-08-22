from django.contrib import admin

from recipes.models import (FavoriteList, Ingredient, Recipe,
                            ShoppingCart, Tag)


# class RecipeIngredientInline(admin.TabularInline):
#     model = RecipeIngredient
#     extra = 1

# @admin.register(RecipeIngredient)
# class RecipeIngredientAdmin(admin.ModelAdmin):
#     pass
class RecipeIngredientInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInLine, )
    # readonly_fields = ('added_in_favorited',)

    # def added_in_favorited(self, obj):
    #     return obj.favorited.count()


# @admin.register(Recipe)
# class RecipeAdmin(admin.ModelAdmin):
#     inlines = (RecipeIngredientInline, )
#     readonly_fields = ('added_in_favorited',)

#     def added_in_favorited(self, obj):
#         return obj.favorited.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(FavoriteList)
class FavoriteListAdmin(admin.ModelAdmin):
    pass


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    pass
