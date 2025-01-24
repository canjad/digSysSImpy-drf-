from rest_framework import mixins
from rest_framework.response import Response
from api.extension import return_code


class DigCreateModelMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # 1. 异常处理
        if not serializer.is_valid():
            return Response({"code": return_code.VALIDATE_ERROR, 'detail': serializer.errors})
        # 2. 优化perform_create
        res = self.perform_create(serializer)
        # 3. 返回数据的处理
        return res or Response({"code": return_code.SUCCESS, 'data': serializer.data})


