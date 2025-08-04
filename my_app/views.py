from django.shortcuts import render
from .utils import scrape_google_results
from .models import SearchResult

def search_view(request):
    results = []
    query = ""

    if request.method == "POST":
        query = request.POST.get("query")
        if query:
            results = scrape_google_results(query)

    # Show latest results (optional)
    recent_results = SearchResult.objects.order_by("-scraped_at")[:20]

    return render(request, "my_app/forms.html", {
        "results": results,
        "query": query,
        "recent_results": recent_results,
    })
