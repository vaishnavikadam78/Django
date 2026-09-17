import logging
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

# FIX 2: Added missing status import
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ItemForm
from .models import Item,Order
from .serializers import ItemSerializer,OrderSerializer
from rest_framework import generics
from rest_framework import viewsets
# Create your views here.
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
#  Into this line:
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
logger = logging.getLogger(__name__)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    #authentication_classes=[TokenAuthentication]
    authentication_classes=[JWTAuthentication]

    #permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    # filterset_fields = ["item_name", "item_price"]  
    # ordering_fields = ["item_name", "item_price"]
    search_fields = ["item_name", "item_price"]
    #def perform_create(self, serializer):
        # serializer.save(user_name=self.request.user)

# class ItemListCreateAPI(generics.ListCreateAPIView):
#     queryset= Item.objects.all()
#     serializer_class = ItemSerializer

# class ItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset=Item.objects.all()
#     serializer_class = ItemSerializer




# class ItemListAPIView(APIView):

#     def get(self, request):
#         # FIX 1: Defined the missing 'items' query variable
#         items = Item.objects.all()
#         serializer = ItemSerializer(items, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)




# @api_view(["GET","POST"])
# def item_list_api(request):
#     if request.method =="GET":
#         items = Item.objects.all()
#         serializer = ItemSerializer(items,many=True)
#         return Response(serializer.data)
#     elif request.method=="POST":
#         serializer = ItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=400)


class ItemDetailAPI(APIView):

    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return None

    def get(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response(
                {"Error": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response(
                {"Error": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response(
                {"Error": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        item.delete()
        return Response(
            {"Message": "Item Deleted"}, status=status.HTTP_204_NO_CONTENT
        )


# @api_view(["GET","PUT","DELETE"])
# def item_detail_api(request,pk):
#     item = Item.objects.get(pk=pk)
#     if request.method == "GET":
#         serializer = ItemSerializer(item)
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = ItemSerializer(item,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#     elif request.method == "DELETE":
#         item.delete()
#         return Response ({"message":"Item Delete"})


# def item_list_json(request):
#     items = Item.objects.all().values(
#         "id",
#         "item_name",
#         "item_desc",
#         "item_price"
#     )

#     return JsonResponse(list(items), safe=False)
# @login_required
# @cache_page(60*15)
# @vary_on_headers("User-Agent")
def index(request):
    logger.info("Fetching all items from the database")
    logger.info(
        f"User{timezone.now().isoformat()} {request.user} requested item list from {request.META.get('REMOTE_ADDR')}"
    )

    item_list = Item.objects.all().order_by("id")

    logger.debug(f"Found {item_list.count()} items")

    paginator = Paginator(item_list, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}

    return render(request, "myapp/index.html", context)


def detail(request, id):
    logger.info(f"Fetching an item with id: {id}")
    try:
        item = get_object_or_404(Item, pk=id)
        logger.debug(f"Item found {item.item_name} (${item.item_price})")
    except Exception as e:
        logger.error(f"Error Fetching the item with id {id}", {e})
        raise
    context = {"item": item}

    return render(request, "myapp/detail.html", context)


def item(request):
    return HttpResponse("Hello, this is item")


def create_item(request):
    form = ItemForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("myapp:index")

    context = {"form": form}

    return render(request, "myapp/item_form.html", context)


# class ItemCreateView(CreateView):
#     model = Item
#     template_name = "myapp/item_form.html"
#     fields = ["item_name", "item_desc", "item_price", "item_image"]

#     def form_valid(self, form):
#         form.instance.user_name = self.request.user
#         return super().form_valid(form)

#     success_url = "/myapp/"


class ItemUpdateView(UpdateView):
    model = Item
    fields = ["item_name", "item_desc", "item_price", "item_image"]
    template_name_suffix = "_update_form"
    # FIX 3: Added missing success redirection URL
    success_url = reverse_lazy("myapp:index")

    def get_queryset(self):
        return Item.objects.filter(user_name=self.request.user)


class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy("myapp:index")

    def get_queryset(self):
        return Item.objects.filter(user_name=self.request.user)


def get_objects(request):
    for item in Item.objects.all():
        print(item.item_name)


def get_objects_optimized(request):
    items = Item.objects.all()

    for item in items:
        print(item.item_name)
