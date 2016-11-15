from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import CaseForm, CoordinateForm, UserForm
from .models import Case, Coordinate


def create_case(request):
    if not request.user.is_authenticated():  # check if the user is authenticated
        return render(request, 'case/login.html')  # if not, send user to login page
    else:
        form = CaseForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            case = form.save(commit=False)
            case.user = request.user
            print('request printed: ')
            print(request.POST)
            case.save()
            return render(request, 'case/detail.html', {'case': case})
        context = {
            "form": form,
        }
        return render(request, 'case/create_case.html', context)


def create_coordinate(request, case_id):
    form = CoordinateForm(request.POST or None, request.FILES or None)
    case = get_object_or_404(Case, pk=case_id)
    if form.is_valid():
        cases_coordinates = case.coordinate_set.all()
        for s in cases_coordinates:
            if s.latitude == form.cleaned_data.get("latitude"):
                context = {
                    'case': case,
                    'form': form,
                    'error_message': 'You already added that coordinate',
                }
                return render(request, 'case/create_coordinate.html', context)
        coordinate = form.save(commit=False)
        coordinate.case = case
        # coordinate.longitude = request.longitude
        coordinate.save()
        return render(request, 'case/detail.html', {'case': case})
    context = {
        'case': case,
        'form': form,
    }
    return render(request, 'case/create_coordinate.html', context)


def delete_case(request, case_id):
    case = Case.objects.get(pk=case_id)
    case.delete()
    cases = Case.objects.filter(user=request.user)
    return render(request, 'case/index.html', {'cases': cases})


def delete_coordinate(request, case_id, coordinate_id):
    case = get_object_or_404(Case, pk=case_id)
    coordinate = Coordinate.objects.get(pk=coordinate_id)
    coordinate.delete()
    return render(request, 'case/detail.html', {'case': case})


def detail(request, case_id):
    if not request.user.is_authenticated():
        return render(request, 'case/login.html')
    else:
        user = request.user
        case = get_object_or_404(Case, pk=case_id)
        return render(request, 'case/detail.html', {'case': case, 'user': user})


def index(request):
    if not request.user.is_authenticated():  # check authentication
        return render(request, 'case/login.html')  # if not logged in, redirect to login page
    else:  # if logged in
        cases = Case.objects.filter(user=request.user)  # find cases for the logged in user
        coordinate_results = Coordinate.objects.all()
        query = request.GET.get("q")
        if query:
            cases = cases.filter(
                Q(watch_id__icontains=query) |
                Q(victim_name__icontains=query)
            ).distinct()
            coordinate_results = coordinate_results.filter(
                Q(latitude__icontains=query)
            ).distinct()
            return render(request, 'case/index.html', {
                'cases': cases,
                'coordinates': coordinate_results,
            })
        else:
            return render(request, 'case/index.html', {'cases': cases})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'case/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                cases = Case.objects.filter(user=request.user)
                return render(request, 'case/index.html', {'cases': cases})
            else:
                return render(request, 'case/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'case/login.html', {'error_message': 'Invalid login'})
    return render(request, 'case/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                cases = Case.objects.filter(user=request.user)
                return render(request, 'case/index.html', {'cases': cases})
    context = {
        "form": form,
    }
    return render(request, 'case/register.html', context)


def coordinates(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'case/login.html')
    else:
        try:
            coordinate_ids = []
            for case in Case.objects.filter(user=request.user):
                for coordinate in case.coordinate_set.all():
                    coordinate_ids.append(coordinate.pk)
            victims_coordinates = Coordinate.objects.filter(pk__in=coordinate_ids)
            # if filter_by == 'favorites':
            #     users_songs = users_songs.filter(is_favorite=True)
        except Case.DoesNotExist:
            victims_coordinates = []
        return render(request, 'case/coordinates.html', {
            'coordinate_list': victims_coordinates,
            'filter_by': filter_by,
        })

# def favorite(request, song_id):
#     song = get_object_or_404(Song, pk=song_id)
#     try:
#         if song.is_favorite:
#             song.is_favorite = False
#         else:
#             song.is_favorite = True
#         song.save()
#     except (KeyError, Song.DoesNotExist):
#         return JsonResponse({'success': False})
#     else:
#         return JsonResponse({'success': True})
#
#
# def favorite_case(request, case_id):
#     case = get_object_or_404(Case, pk=case_id)
#     try:
#         if case.is_favorite:
#             case.is_favorite = False
#         else:
#             case.is_favorite = True
#         case.save()
#     except (KeyError, Case.DoesNotExist):
#         return JsonResponse({'success': False})
#     else:
#         return JsonResponse({'success': True})

