class MultiSerializerMixin:

    def get_serializer_class(self):
        return self.serializer_classes[self.action]

