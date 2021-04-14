from .forms import SearchForm


def context_processor_middleware(request):
    context = {
        'search_form': SearchForm(),
    }
    return context

