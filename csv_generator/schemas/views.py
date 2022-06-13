from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


from .models import Schema, DataSet, Column
from .forms import ColumnFormset, SchemaForm, ColumnEditFormset
from .tasks import generate_fake_data


class SchemaListView(LoginRequiredMixin, ListView):
    login_url = '/'

    context_object_name = 'data_schemas'

    def get_queryset(self):
        return Schema.objects.filter(user=self.request.user)


class SchemaCreateView(LoginRequiredMixin, CreateView):
    """Create View for both Schema and corresponding Columns models."""
    login_url = '/'

    form_class = SchemaForm
    formset_class = ColumnFormset(queryset=Column.objects.none())
    queryset = Schema.objects.all()

    def get_context_data(self, **kwargs):
      context = super(SchemaCreateView, self).get_context_data(**kwargs)
      context['formset'] = ColumnFormset(queryset=Column.objects.none())

      return context

    def form_valid(self, form):
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = ColumnFormset(request.POST)
        print(form.errors)
        if form.is_valid() and formset.is_valid():
            form.instance.user = request.user
            form.save(commit=True)
            for column in formset:
                column.instance.schema = form.instance
                column.save(commit=True)

            return redirect('home')
        return render(request, self.template_name, 
                      {'form': form, 'formset': formset})

    def get_success_url(self) -> str:
        return reverse('home')
    

class SchemaEditView(LoginRequiredMixin, UpdateView):
    """Edit View for both Schema and corresponding Columns models."""
    login_url = '/'

    model = Schema
    form_class = SchemaForm

    def get_context_data(self, **kwargs):
      context = super(SchemaEditView, self).get_context_data(**kwargs)
      context['formset'] = ColumnEditFormset(
          queryset=Column.objects.filter(schema=self.get_object()))

      return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.instance.user = request.user
        formset = ColumnEditFormset(request.POST)
        if form.is_valid():
            form.save(commit=True)
            for column in formset:
                column.instance.schema = form.instance
                if column.is_valid():
                    column.save(commit=True)
            return redirect('home')
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def get_success_url(self) -> str:
        return reverse('home')


class SchemaDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/'

    model = Schema
    success_url = reverse_lazy('home')


class DataSetListView(LoginRequiredMixin, ListView):
    login_url = '/'

    def get_queryset(self):
        return DataSet.objects.filter(schema=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schema'] = self.kwargs.get('pk')
        return context 


@login_required
def dataset_generate(request):
    """Get arguments from request and call fake data generation celery worker."""
    login_url = '/'

    if request.method == 'POST':
        row_number = request.POST['row_number']
        schema_id = request.POST['schema_id']
        schema = get_object_or_404(Schema, pk=schema_id)
        dataset = DataSet(schema=schema)
        dataset.save()
        generate_fake_data.delay(int(row_number), schema_id, dataset.id)
        
        return HttpResponseRedirect(f'/schema/{schema_id}/datasets/')