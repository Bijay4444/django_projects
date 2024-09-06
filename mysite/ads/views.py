from django.shortcuts import render, redirect, get_object_or_404
from .owner import OwnerCreateView, OwnerListView, OwnerDetailView, OwnerUpdateView, OwnerDeleteView
from .models import Ad, Comment, Fav
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Q

from ads.forms import CreateForm, CommentForm

#disableling csrfvalidation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

# Create your views here.
class AdListView(OwnerListView):
    model = Ad
    template_name= 'ads/ad_list.html'

    def get(self, request):
        ad_list = Ad.objects.all()
        favourites = list()
        strval = request.GET.get("search", False)

        if request.user.is_authenticated:
            rows = request.user.favourite_ads.values('id')
            favourites = [row['id'] for row in rows]

        if strval:
            query = Q(title__icontains=strval)
            query.add(Q(text__icontains=strval),Q.OR)
            ad_list = Ad.objects.filter(query).select_related().distinct().order_by('-updated_at')[:10]
        else:
            ad_list = Ad.objects.all().order_by('-updated_at')[:10]

        context = {'ad_list': ad_list, 'favourites': favourites, 'search': strval}
        return render(request, self.template_name, context)

class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        comments = Comment.objects.filter(ad=ad).order_by('-updated_at')
        comment_form = CommentForm()
        context = {'ad': ad, 'comments': comments, 'comment_form': comment_form}
        return render(request, self.template_name, context)

class AdCreateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('myads:all')

    def get(self, request, pk=None):
        form = CreateForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            context={'form': form}
            return render(request, self.template_name, context)

        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        form.save_m2m()

        return redirect(self.success_url)

class AdUpdateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('myads:all')

    def get(self, request, pk):
        pic = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=pic)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        pic = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid():
            context={'form': form}
            return render(request, self.template_name, context)

        pic = form.save(commit=False)
        pic.save()

        return redirect(self.success_url)

class AdDeleteView(OwnerDeleteView):
    model = Ad

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        comment = Comment(text= request.POST['comment'], owner=request.user, ad=ad)
        comment.save()
        return redirect(reverse('myads:ad_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/comment_delete.html"

    def get_success_url(self):
        ad = self.object.ad
        return reverse('myads:ad_detail', args=[ad.id])

@method_decorator(csrf_exempt, name='dispatch')
class AddFavouriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print("Add PK", pk)
        t = get_object_or_404(Ad, id=pk)
        fav = Fav(user=request.user, ad=t)

        try:
            fav.save()
        except IntegrityError:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavouriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print("Delete PK", pk)
        t = get_object_or_404(Ad, id=pk)

        try:
            Fav.objects.get(user=request.user, ad=t).delete()
        except Fav.DoesNotExist:
            pass

        return HttpResponse()


def stream_file(request, pk):
    pic = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response