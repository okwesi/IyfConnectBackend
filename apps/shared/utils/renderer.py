from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    """
        Custom JSONRenderer that adds 'results' key to the response data if the data is a list of dictionaries.
        Example:
            {
                "results": [
                    {"id": 1, "name": "John"},
                    {"id": 2, "name": "Jane"}
                ]
            }
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            data = {'results': data}
        return super().render(data, accepted_media_type, renderer_context)
