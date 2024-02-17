from django.shortcuts import render, redirect
from django.views.generic import (TemplateView, DetailView,
                                  ListView, CreateView,
                                  UpdateView, DeleteView, FormView,)


from .models import Standard, Subject, Lesson
from django.urls import reverse_lazy
from .forms import CommentForm, ReplyForm, LessonForm
from django.http import HttpResponseRedirect
# фишки

from django.contrib.auth.decorators import login_required



class StandardListView(ListView):
    context_object_name = 'standards'
    model = Standard
    template_name = 'educate_portal/standard_list_view.html'


class SubjectListView(DetailView):
    context_object_name = 'standards'

    model = Standard
    template_name = 'educate_portal/subject_list_view.html'


class LessonListView(DetailView):
    context_object_name = 'subjects'
    model = Subject
    template_name = 'educate_portal/lesson_list_view.html'


class LessonDetailView(DetailView, FormView):
    context_object_name = 'lessons'
    model = Lesson
    template_name = 'educate_portal/lesson_detail_view.html'
    form_class = CommentForm
    second_form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(request=self.request)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(request=self.request)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'

        form = self.get_form(form_class)

        if form_name == 'form' and form.is_valid():
            print("comment form is returned")
            return self.form_valid(form)
        elif form_name == 'form2' and form.is_valid():
            print("reply form is returned")
            return self.form2_valid(form)

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.Standard
        subject = self.object.subject
        return reverse_lazy('educate_portal:lesson_detail', kwargs={'standard': standard.slug,
                                                                    'subject': subject.slug,
                                                                    'slug': self.object.slug})

    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.lesson_name = self.object.comments.name
        fm.lesson_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())


from django.contrib import messages

class LessonCreateView(CreateView):

    form_class = LessonForm
    context_object_name = 'subject'
    model = Subject
    template_name = 'educate_portal/lesson_create.html'

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.standard
        return reverse_lazy('educate_portal:lesson_list', kwargs={'standard': standard.slug,
                                                                  'slug': self.object.slug})

    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.Standard = self.object.standard
        fm.subject = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())


class LessonUpdateView(UpdateView):
    fields = ('name', 'position', 'description',
              'description2', 'file', 'ppt', 'Notes')
    model = Lesson
    template_name = 'educate_portal/lesson_update.html'
    context_object_name = 'lessons'


class LessonDeleteView(DeleteView):
    model = Lesson
    context_object_name = 'lessons'
    template_name = 'educate_portal/lesson_delete.html'

    def get_success_url(self):
        print(self.object)
        standard = self.object.Standard
        subject = self.object.subject
        return reverse_lazy('educate_portal:lesson_list', kwargs={'standard': standard.slug, 'slug': subject.slug})

from django.shortcuts import render, redirect

# def become_teacher(request):
#     if request.method == 'POST' and 'become_teacher' in request.POST:
#         user_profile = request.user.profile
#         user_profile.is_teacher = True
#         user_profile.save()
#         return redirect('educate_portal:lesson_list')

#     # Handle the case where the form is not submitted
#     return render(request, 'lesson_list.html')



