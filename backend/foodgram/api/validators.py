from django.core.exceptions import ValidationError


def validate_tags(value):
    tags_list = []
    for tag in value:
        if not tag:
            raise ValidationError(
                'Укажите как минимум один тэг'
            )
        if tag in tags_list:
            raise ValidationError(
                'Этот тэг уже используется'
            )
        tags_list.append(tag)
    return value


def validate_ingredients(ingredients):
    if not ingredients:
        raise ValidationError('Ингредиенты не добавлены.')

    ingredients_list = []
    for ingredient in ingredients:
        ingredient_id = ingredient.get('id')
        if ingredient_id in ingredients_list:
            raise ValidationError(
                'Не может быть двух одинаковых ингредиентов.'
            )
        ingredients_list.append(ingredient_id)

        amount = int(ingredient.get('amount'))
        if amount < 1:
            raise ValidationError(
                'Количество ингредиентов должно быть больше 1'
            )
    return ingredients


def validate_cooking_time(cooking_time):
    if int(cooking_time) < 1:
        raise ValidationError(
            'Время приготовления должно быть больше 0'
        )
    return cooking_time
