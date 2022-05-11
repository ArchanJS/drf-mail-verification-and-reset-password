from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import User

class CustomAuthToken(ObtainAuthToken):
    def post(self,request,*args,**kwargs):
        try:
            user_data=User.objects.filter(email=request.data['username']).values()[0]
            serializer=self.serializer_class(data=user_data,context={'request':request})
            serializer.is_valid(raise_exception=True)
            print(user_data)
            user=serializer.validated_data['user']
            token,created=Token.objects.get_or_create(user=user)
            return Response({
                'token':token.key,
                'user_id':user.pk,
                'email':user.email
            })
        except Exception as e:
            print(e)
            return Response({
                'error':'Something went wrong!'
            })