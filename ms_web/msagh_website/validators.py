from django.core.exceptions import ValidationError

def validate_size(image):
    """Validator for image size in meme section"""

    print(image.size)
    error = False

    if image.size > 250000:
        error = True

    if error:
        raise ValidationError(
            [f'Maksymalny rozmiar obrazka to 150kb.']
        )


def validate_shape(image):
    """Validator for image shape in meme section"""
    print(image.width, " ", image.height)
    error = False
    if not (400 < image.width < 950):
        error = True
    if not (400 < image.height < 950):
        error = True

    if error:
        raise ValidationError(
            [f'Zły rozmiar obrazka.']
        )


