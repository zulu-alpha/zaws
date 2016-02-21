from wtforms.validators import ValidationError


class Unique:
    """Checks if the given value is unique in the given model"""
    def __init__(self, model, db_field, exclude=False, message='This has already been taken!'):
        """
        :param model: Model object to check in
        :param db_field: The field type in the Model to check
        :param exclude: Whether or not to exclude the object id found in the 'exclude_id' field
        :param message: Optional message for validation error
        :return: None
        """
        self.model = model
        self.db_field = db_field
        self.exclude = exclude
        self.message = message

    def __call__(self, form, field):
        instance = self.model.objects(__raw__={self.db_field: field.data}).first()
        if instance:
            if self.exclude and not instance.id == form.exclude_id.data:
                raise ValidationError(self.message)
            elif not self.exclude:
                raise ValidationError(self.message)


class Exists:
    """Checks if the given value exists in the given model"""
    def __init__(self, model, db_field, message="This doesn't exist!"):
        """
        :param model: Model object to check in
        :param db_field: The field type in the Model to check
        :param message: Optional message for validation error
        :return: None
        """
        self.model = model
        self.db_field = db_field
        self.message = message

    def __call__(self, form, field):
        instance = self.model.objects(__raw__={self.db_field: field.data}).first()
        if not instance:
            raise ValidationError(self.message)


class ExistsList:
    """Checks if any given value in the list exists in the given model"""
    def __init__(self, model, db_field, message="This doesn't exist!"):
        """
        :param model: Model object to check in
        :param db_field: The field type in the Model to check
        :param message: Optional message for validation error
        :return: None
        """
        self.model = model
        self.db_field = db_field
        self.message = message

    def __call__(self, form, field):
        for item in field.data:
            instance = self.model.objects(__raw__={self.db_field: item}).first()
            if not instance:
                raise ValidationError(self.message)
