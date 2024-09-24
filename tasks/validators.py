from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_image(image):
    if image.size > 10 * 1024 * 1024:  # Limit image size to 10MB
        raise ValidationError(_("Image size should not exceed 10 MB."))
    if not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise ValidationError(_("Only .jpg, .jpeg, and .png formats are allowed."))
