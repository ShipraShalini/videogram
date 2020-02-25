from rest_framework.response import Response


class JSONResponse(Response):

    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False):
        super().__init__(
            data=data,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type='application/json'
        )

