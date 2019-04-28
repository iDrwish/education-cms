from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    """

    This is our custom OrderField. It inherits from the
    PositiveIntegerField field provided by Django.
    Our OrderField field takes an optional for_fields parameter that
    allows us to indicate the fields that the order has to be
    calculated with respect to.
    \n
    Our field overrides the pre_save() method of the
    PositiveIntegerField field, which is executed before saving the
    field into the database. In this method, we perform the
    following actions:
    1. We check if a value already exists for this field in the model
     instance. We use self.attname, which is the attribute name
     given to the field in the model.
     If the attribute's value is different than None,
     we calculate the order we should give it as follows:
        1. We build a QuerySet to retrieve all objects for the field's model.
        We retrieve the model class the field belongs to by accessing self.model.
        2. We filter the QuerySet by the fields' current value for the model fields that are defined in the for_fields parameter of the field, if any. By doing so, we calculate the order with respect to the given fields.
        3. We retrieve the object with the highest order with last_item = qs.latest(self.attname) from the database. If no object is found, we assume this object is the first one and assign the order 0 to it.
        4. If an object is found, we add 1 to the highest order found.
        5. We assign the calculated order to the field's value in the model
    instance using setattr()and return it.
    2. If the model instance has a value for the current field, we don't do anything.
    \n
    Arguments:
        models {[type]} -- [description]
    \n
    Returns:
        [type] -- [description]
    """
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # No current value
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # filter by objects with the same
                    # fields value
                    query = {
                        field: getattr(model_instance, field)
                        for field in self.for_fields}
                    qs = qs.filter(**query)
                # get the last item
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            # Set the order value
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(OrderField, self).pre_save(model_instance, add)
