from django.contrib import admin

from recipes.models import (FavoriteList, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)


# class RecipeIngredientInline(admin.TabularInline):
#     model = RecipeIngredient
#     extra = 1

# @admin.register(RecipeIngredient)
# class RecipeIngredientAdmin(admin.ModelAdmin):
#     pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # inline = RecipeIngredientAdmin
    inline = RecipeIngredient
    readonly_fields = ('added_in_favorited',)

    def added_in_favorited(self, obj):
        return obj.favorited.count()


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
