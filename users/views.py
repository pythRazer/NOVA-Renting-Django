from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from actions.models import Action
from nova.models import admin_user, regular_user


def profile(request, username):
    user1 = get_object_or_404(User, username=username)
    actions = Action.objects.filter(user=user1).order_by('-created')[:15]
    # actions = Action.objects.all().order_by('-created')[:15]
    return render(request, "users/user/profile.html", {"user": user1, "actions": actions})


def edit_profile(request, username):
    if not request.session.get('username', False):
        return redirect('users:log-in-page')

    else:
        user1 = get_object_or_404(User, username=username)

    if request.session.get('username') == username or request.session.get('role') == 'admin':

        if request.method == 'POST':

            # id
            # username = request.POST.get('edit-username')
            # user1.username = username
            email = request.POST.get('edit-email')
            user1.email = email
            first_name = request.POST.get('edit-first-name')
            user1.first_name = first_name
            last_name = request.POST.get('edit-last-name')
            user1.last_name = last_name
            subscription = request.POST.get('edit-subscription')
            user1.details.subscription = subscription
            # print(user1.details.role)

            if request.session.get('username') == username:
                new_password = request.POST.get('edit-password')
                # user1.password = new_password
                user1.set_password(new_password)

            if request.session.get('role') == 'admin':
                role = request.POST.get('edit-role')

                # print(role)
                # print(user1.details.role)
                if user1.details.role != role:
                    user1.details.role = role
                    action = Action(
                        user=User.objects.get(username=request.session.get("username")),
                        verb="changed the role of",
                        target=user1
                    )
                    action.save()


            user1.save()
            print(user1.username, "'s profile has been edited")
            return redirect("users:profile", user1.username)
        else:

            return render(request, "users/user/edit-profile.html", {"user": user1})
    else:


        actions = Action.objects.filter(user=user1).order_by('-created')[:15]
        # actions = Action.objects.all().order_by('-created')[:15]
        return render(request, "users/user/profile.html", {"user": user1, "actions": actions})

















# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST.get('register-username')
        email = request.POST.get('register-email')
        password = request.POST.get('register-password')
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email):
            # messages.error(request, "Username '%s' is already taken. Please choose a different one." % username)
            return render(request, "users/user/register.html", {'error': 'Username or email already taken'})
        else:
            user = User.objects.create_user(username, email, password)
            messages.add_message(request, messages.SUCCESS,
                                 "You successfully registered with the username: %s" % user.username)
            user = authenticate(username=username, password=password)
            if user is not None:
                request.session['username'] = user.username
                request.session['role'] = user.details.role
                return redirect('nova:properties-list')
            return redirect('nova:properties-list')

    else:
        return render(request, "users/user/register.html")


def login(request):
    username = request.POST.get("username")
    pw = request.POST.get("pw")

    user = authenticate(username=username, password=pw)
    if user is not None:
        request.session['username'] = user.username
        request.session['role'] = user.details.role
        return redirect('nova:properties-list')
    else:
        context = {'error': 'Incorrect username or password.'}
        return render(request, "users/user/login.html", context)
        # messages.add_message(request, messages.SUCCESS,
        #                      "Invalid username or password.")

    # if (username == admin_user['username']) and (pw == admin_user['password']):
    #
    #
    #     return redirect('nova:properties-list')
    # elif (username == regular_user['username']) and (pw == regular_user['password']):
    #     request.session['username'] = username
    #     request.session['role'] = 'regular'
    #     return redirect('nova:properties-list')
    #
    # else:
    #     # messages.add_message(request, messages.WARNING, "Incorrect username or password.")
    #     # Incorrect username/password, do not redirect but render the login page with an error
    #     context = {'error': 'Incorrect username or password.'}
    #     return render(request, "users/user/login.html", context)

    # return redirect('nova:log-in-page')


def logout(request):
    del request.session['username']
    del request.session['role']
    return redirect('nova:home-page')


def log_in_page(request):
    return render(request, "users/user/login.html")
