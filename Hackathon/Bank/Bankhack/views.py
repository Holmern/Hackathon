from rest_framework.views import APIView
from django.shortcuts import redirect, render, reverse, get_object_or_404
from rest_framework import generics, permissions

class login(APIView):
    permissions_classes = [permissions.IsAuthenticated, ]
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/bankapp/')
        else:    
            return redirect('/mfa/')
