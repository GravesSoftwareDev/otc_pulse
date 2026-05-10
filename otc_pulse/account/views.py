import io
import qrcode
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.urls import reverse
from .forms import UserRegistrationForm, ProfileRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from bulletin_board.models import Request, Reservation


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('account:login')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()
    return render(
        request,
        'account/register.html',
        {'user_form':user_form, 'profile_form':profile_form, 'section':'account'}
    )

@login_required
def profile(request):
    profile = request.user.profile
    if profile.role == profile.Role.ADMIN:
        base_requests = Request.objects.all()
    else:
        clubs = profile.club_officer.all() | profile.faculty_advisor.all()
        base_requests = Request.objects.filter(club__in=clubs)

    club_requests = {
        'pending': base_requests.filter(approval_status='-').order_by('due_date'),
        'approved': base_requests.filter(approval_status='O').order_by('due_date'),
        'denied': base_requests.filter(approval_status='X').order_by('due_date'),
    }

    club_count = (
        profile.club_member.all() | profile.faculty_advisor.all()
    ).distinct().count()

    reservations = (
        Reservation.objects.select_related('event', 'club', 'location').order_by('event__start_time')
        if profile.role == profile.Role.ADMIN
        else None
    )

    return render(request, 'account/profile.html', {
        'profile': profile,
        'club_requests': club_requests,
        'reservations': reservations,
        'is_admin': profile.role == profile.Role.ADMIN,
        'club_count': club_count,
    })

@login_required
def my_qr_page(request):
    profile = request.user.profile
    return render(request, 'account/my_qr.html', {
        'profile': profile,
        'section': 'account',
    })


@login_required
def my_qr_image(request):
    profile = request.user.profile
    img = qrcode.make(profile.short_code)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png')


@login_required
def manage_users(request):
    profile = request.user.profile
    if profile.role != profile.Role.ADMIN:
        raise PermissionDenied

    q = request.GET.get('q', '').strip()
    results = None
    if q:
        results = (
            Profile.objects.select_related('user')
            .filter(
                Q(user__first_name__icontains=q) |
                Q(user__last_name__icontains=q) |
                Q(user__username__icontains=q) |
                Q(otc_email__icontains=q)
            )
            .exclude(pk=profile.pk)
            .order_by('user__last_name', 'user__first_name')
        )

    return render(request, 'account/manage_users.html', {
        'results': results,
        'q': q,
        'roles': Profile.Role.choices,
        'section': 'account',
    })


@login_required
def set_role(request, profile_pk):
    if request.user.profile.role != request.user.profile.Role.ADMIN:
        raise PermissionDenied
    if request.method == 'POST':
        target = get_object_or_404(Profile, pk=profile_pk)
        new_role = request.POST.get('role')
        valid_roles = [r[0] for r in Profile.Role.choices]
        if new_role in valid_roles:
            target.role = new_role
            target.save(update_fields=['role'])
            messages.success(request, f'{target} has been updated to {target.get_role_display()}.')
    q = request.POST.get('q', '')
    url = reverse('account:manage_users')
    if q:
        url += f'?q={q}'
    return redirect(url)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            instance = request.user,
            data = request.POST
        )
        profile_form = ProfileEditForm(
            instance = request.user.profile,
            data = request.POST,
            files = request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard:home')
        else:
            messages.error(request, 'There was an error updating your profile.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance = request.user.profile)
    return render(
        request,
        'account/edit_profile.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'section': 'account',
        }
    )
