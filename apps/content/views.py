from django.conf import settings
from django.views import generic
from django.shortcuts import render, get_object_or_404
from .models import Course, Video, Product
from apps.shopping_cart.models import Order, OrderItem
# Create your views here.

"""
class CourseListView(generic.ListView):
    template_name = "content/course_list.html"
    queryset = Course.objects.all()
    paginate_by = 10

class CourseDetailView(generic.DetailView):
    template_name = "content/course_detail.html"
    queryset = Course.objects.all()
    """

class ProductListView(generic.ListView):
    template_name = "content/product_list.html"
    queryset = Product.objects.all()
    #paginate_by = 10

class ProductDetailView(generic.DetailView):
    template_name="content/product_detail.html"
    queryset = Product.objects.all()

#variables globales para defenir la relacion en CourseDetailView
#en lugar del booleano q habia
# y se crea la funcion check_course_relationship para que haga esa tarea
OWNED = 'owned'
IN_CART = 'in_cart'
NOT_IN_CART = 'not_in_cart'

#adaptar a userprofile == userlibrary
def check_course_relationship(request, course):
    if course in request.user.userprofile.cursos.all():
        return OWNED
    order_qs=Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        order_item_qs = OrderItem.objects.filter(course=course)
        if order_item_qs.exists():
            order_item = order_item_qs[0]
            if order_item in order.items.all():
                return IN_CART
    return NOT_IN_CART




def CourseListView(request):
    courses=Course.objects.all()
    #falta adaptar algo como en coursedetailview para que una vez en el carrito
    #saque la opcion de añadir al carrito
    """order = Order.objects.get(user=request.user)
    order_item = OrderItem.objects.get(course=course)
    course_is_in_cart=False
    if order_item in order.items.all():
        course_is_in_cart=True"""
    context={
        'courses':courses,
        #'in_cart':course_is_in_cart
    }
    return render(request, 'content/course_list.html', context)

def CourseDetailView(request, slug):
    #display a list of the chapter in this book
    course=get_object_or_404(Course.objects.all(), slug=slug)
    course_status = check_course_relationship(request, course)
    context={
        'course':course,
        'course_status':course_status
    }
    return render(request, "content/course_detail.html", context)

class VideoDetailView(generic.DetailView):
    template_name = "content/video_detail.html"


    def get_object(self):
        video = get_object_or_404(Video, slug=self.kwargs["video_slug"])
        return video

    #query set es el nombre que figura en la barra de navegador
    def get_queryset(self):
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        return course.videos.all()
        #el return es para que devuelva todos los videos que pertenecen al curso
