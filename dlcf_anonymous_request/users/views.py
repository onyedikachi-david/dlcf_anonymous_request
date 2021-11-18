from datetime import time

from django.contrib.auth import get_user_model
from dlcf_anonymous_request.users.models import AnonymousMessage
from dlcf_anonymous_request.users.forms import RequestCreateForm
from django.shortcuts import render
# from django.urls import reverse

from django.forms.models import BaseModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView
from django.http import HttpResponse, HttpResponseRedirect

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class RequestCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': RequestCreateForm()}
        return render(request, 'pages/home.html', context)

    def post(self, request, *args, **kwargs):
        form = RequestCreateForm(request.POST)
        if form.is_valid():
            book = form.save()
            book.save()
            return HttpResponseRedirect(reverse_lazy('request_form_sub_success'))
        return render(request, 'pages/home.html', {'form': form})


# class RequestCreateView(CreateView):
#     model = AnonymousMessage
#     # form_class = RequestCreateForm
#     template_name = "pages/home.html"
#     fields = ['request']

# def form_valid(self, form: BaseModelForm) -> HttpResponse:
#     request_form = form.save()
#     response = HttpResponse()
#     # response["HX-Trigger"] = json.dumps(
#     #     {"redirect": {"url": request_form_sub_success}}
#     # )
#     return response

request_create_view = RequestCreateView.as_view()


# def request_create_view(request, pk):
#     # author = Author.objects.get(id=pk)
#     model = AnonymousMessage
#     # books = Book.objects.filter(author=author)
#     # form = BookForm(request.POST or None)
#     form = RequestCreateForm

#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             # book.author = author
#             # book.save()
#             return redirect("success")
#         else:
#             return render(request, "pages/home.html", context={
#                 "form": form
#             })

#     context = {
#         "form": form,
#         # "author": author,
#         # "books": books
#     }

#     return render(request, "pages/home.html", context)


def request_successful_submit(request):
    return render(request, "pages/success.html")


def export_audits_as_pdf(self, request, queryset):
    file_name = "prayer_request{0}.pdf".format(time.hour)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(file_name)

    data = [['request']]
    for d in queryset.all():
        # datetime_str = str(d.action_time).split('.')[0]
        item = [d.request]
        data.append(item)
        print(d)
        print(data)

    doc = SimpleDocTemplate(response, pagesize=(21 * inch, 29 * inch))
    elements = []

    table_data = Table(data)
    table_data.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                    ("FONTSIZE", (0, 0), (-1, -1), 13)]))
    elements.append(table_data)
    doc.build(elements)

    return response
