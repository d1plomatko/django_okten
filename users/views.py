import json
from rest_framework.views import APIView
from rest_framework.response import Response


class ReadWriteFile:
    _file = None

    @classmethod
    def read_file(cls):
        try:
            with open(cls._file) as file:
                return json.load(file)

        except (Exception,):
            return []

    @classmethod
    def write_file(cls, data):
        try:
            with open(cls._file, 'w') as file:
                json.dump(data, file)
        except Exception as err:
            return str(err)


class MyApiView(APIView, ReadWriteFile):
    _file = 'users.json'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.users = self.read_file()


class UsersListCreateView(MyApiView):

    def get(self, *args, **kwargs):
        return Response(self.users)

    def post(self, *args, **kwargs):
        data = self.request.data
        data['id'] = self.users[-1]['id'] + 1 if self.users else 1
        self.users.append(data)
        self.write_file(self.users)
        return Response(data)


class UsersRetrieveUpdateDestroyView(MyApiView):

    def get(self, *args, **kwargs):
        pk = kwargs.get('pk')
        user = self.get_user_by_pk(pk)

        if user is None:
            return Response('Not Found')

        return Response(user)

    def put(self, *args, **kwargs):
        pk = kwargs.get('pk')
        user = self.get_user_by_pk(pk)

        if user is None:
            return Response('Not Found')

        data = self.request.data

        if data.get('id'):
            del data['id']

        user |= data

        self.write_file(self.users)
        return Response(user)

    def delete(self, *args, **kwargs):
        pk = kwargs.get('pk')
        index = next((i for i, u in enumerate(self.users) if u['id'] == pk), None)

        if index is None:
            return Response('Not Found')

        del self.users[index]
        self.write_file(self.users)

        return Response('deleted')

    def get_user_by_pk(self, pk):
        return next((user for user in self.users if user['id'] == pk), None)
