from django.contrib.auth.models import User
from django.db.models import Avg
from django.db.models.functions import Coalesce
from django.db.models import Avg, Value, FloatField
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from actions.models import Action
from .models import regular_user, admin_user, Property, Comments
from datetime import datetime
from django.contrib import messages
from django.utils.timesince import timesince


# Home page if log in: user dashboard, if not: ad welcome page
def home_page(request):
    if not request.session.get('username', False):
        return render(request, "nova/property/home.html")
    else:
        properties = Property.objects.all()
        user = User.objects.get(username=request.session.get('username'))
        own_actions = Action.objects.filter(user=user)

        user_properties = Property.objects.filter(user=user)

        related_actions = Action.objects.filter(target_id=user.id, verb="changed the role of")

        for property in user_properties:
            actions_for_property = Action.objects.filter(target_id=property.id)
            related_actions = related_actions | actions_for_property

        combined_actions = own_actions | related_actions
        return_actions = combined_actions.order_by('-created')[:15]


        return render(request, "nova/property/home-logged-in.html", {"properties": properties, "actions": return_actions})


def properties_list(request):
    sort_by = request.GET.get('sort', 'availability')  # default sort is by 'date_posted'

    # Use Coalesce to set the default average rating to 0 (If no ratings)
    properties = Property.objects.annotate(
        average_rating=Coalesce(Avg('comments__rating'), Value(0), output_field=FloatField())
    )

    if sort_by == 'house_name':
        # properties = Property.objects.all().order_by('house_name')
        properties = properties.order_by('house_name')
    elif sort_by == 'rent_cost':
        # properties = Property.objects.all().order_by('rent_cost')
        properties = properties.order_by('rent_cost')
    else:
        # properties = Property.objects.all().order_by('-availability')  # '-' indicates descending order
        properties = properties.order_by('-availability')  # '-' indicates descending order
    return render(request, "nova/property/list.html", {"properties": properties})


def property_detail(request, property_id):
    properties = Property.objects.annotate(
        average_rating=Coalesce(Avg('comments__rating'), Value(0), output_field=FloatField())
    )
    property = get_object_or_404(Property, id=property_id)
    comments = property.comments.all()
    comments = comments.order_by('-date_posted')
    # Calculate the average rating if there are reviews
    average_rating = comments.aggregate(Avg('rating'))['rating__avg']
    if average_rating is not None:
        average_rating = round(average_rating, 1)

    for property in properties:
        if property.id == property_id:
            # comments = Comments.objects.get(property)
            break

    return render(request,
                  "nova/property/detail.html",
                  {"property": property, "comments": comments, "average_rating": average_rating})


# Log in for regular user or admin user, determine which kind of the user is logged in


# Post a property (only for who is logged in)
def post_property_page(request):
    if not request.session.get('username', False):
        return redirect('users:log-in-page')
    if request.method == 'POST':
        # process the form
        # id
        house_name = request.POST.get('add-house-name')
        address = request.POST.get('add-address')
        availability = request.POST.get('add-availability')
        bathrooms_count = request.POST.get('add-bathrooms-count')
        bedrooms_count = request.POST.get('add-bedrooms-count')
        city = request.POST.get('add-city')
        date_posted = datetime.now()
        description = request.POST.get('add-description')
        finding_rm = False
        floor = request.POST.get('add-floor')
        initial_fee = request.POST.get('add-initial-fee')
        is_verified = False
        poster = request.POST.get('add-poster')
        # rating = 0.0
        rent_cost = request.POST.get('add-rent-cost')
        size = request.POST.get('add-size')
        unit = request.POST.get('add-unit')
        wished = "admin"
        zip_code = request.POST.get('add-zip-code')
        photo = request.FILES.get('add-photo')
        print(photo)
        np = Property(

            house_name=house_name,
            address=address,
            availability=availability,
            bathrooms_count=bathrooms_count,
            bedrooms_count=bedrooms_count,
            city=city,
            date_posted=date_posted,
            description=description,
            finding_rm=finding_rm,
            floor=floor,
            initial_fee=initial_fee,
            is_verified=is_verified,
            poster=poster,
            # rating=rating,
            rent_cost=rent_cost,
            size=size,
            unit=unit,
            # url=url,
            # wished=wished,
            zip_code=zip_code,
            photo=photo,
            user=User.objects.get(username=request.session.get("username"))

        )
        # Save to database
        np.save()

        action = Action(
            user=User.objects.get(username=request.session.get("username")),
            verb="posted a new house",
            target=np
        )
        action.save()

        # Message for indicating the status
        messages.add_message(request, messages.SUCCESS, "You successfully posted a new property: %s" % np.house_name)
        print(house_name, "has been posted")

        return redirect("nova:property-detail", np.id)
    else:
        return render(request, "nova/property/post.html")


# def user_home(request):
#     return render(request, "nova/property/home-logged-in.html", {"properties": properties})


def search_result(request):
    return render(request, "nova/property/search-result.html")


# Delete property URL is only accessible for admin user, regular user can't access only be redirected to the list
# page, and logged-in user will be navigated to the login page
def delete_property(request, property_id):
    property_to_delete = Property.objects.get(id=property_id)
    property_title = property_to_delete.house_name
    print(request.session.get("username"))
    print(property_to_delete.user.username)
    if not request.session.get('username', False):
        print("Please log in")
        return redirect('users:log-in-page')
    elif not request.session['role'] == 'admin' and request.session.get("username") != property_to_delete.user.username:
        print("You don't have permission, not admin")
        return redirect('nova:properties-list')
    elif request.session.get("username") != property_to_delete.user.username:
        print("You don't have permission to delete others' posts")
    else:
        action = Action(
            user=User.objects.get(username=request.session.get("username")),
            verb="deleted the house",
            target=property_to_delete,
            deleted_house_name=property_to_delete.house_name
        )
        action.save()

        # Delete the property
        property_to_delete.delete()

        print("Property id", property_id, "has been deleted")
        messages.add_message(request, messages.WARNING, "You deleted a property: %s" % property_title)

        # TODO:Delete operation
        return redirect('nova:properties-list')


def about(request):
    return render(request, "nova/about.html")


# Only logged in user can edit the property, clicking the corresponded property in the home page will leads to the edit page
def edit_property_page(request, property_id):
    if not request.session.get('username', False):
        return redirect('users:log-in-page')
    if request.method == 'POST':
        properties = Property.objects.all()
        for property in properties:
            if property.id == property_id:
                break

        if not request.session.get('username', False):
            return redirect('users:log-in-page')
        if request.method == 'POST':
            # process the form
            # id
            house_name = request.POST.get('edit-house-name')
            if property.house_name != house_name:
                action = Action(
                    user=User.objects.get(username=request.session.get("username")),
                    verb="edited the house title",
                    target=property
                )
                action.save()
            property.house_name = house_name
            address = request.POST.get('edit-address')
            property.address = address
            availability = request.POST.get('edit-availability')
            property.availability = availability
            bathrooms_count = request.POST.get('edit-bathrooms-count')
            property.bathrooms_count = bathrooms_count
            bedrooms_count = request.POST.get('edit-bedrooms-count')
            property.bedrooms_count = bedrooms_count
            city = request.POST.get('edit-city')
            property.city = city
            # date_posted = datetime.now()
            # property.date_posted = datetime.now()
            description = request.POST.get('edit-description')
            if property.description != description:
                action = Action(
                    user=User.objects.get(username=request.session.get("username")),
                    verb="edited the house description",
                    target=property
                )
                action.save()
            property.description = description
            # finding_rm = False
            floor = request.POST.get('edit-floor')
            property.floor = floor
            initial_fee = request.POST.get('edit-initial-fee')
            property.initial_fee = initial_fee
            # is_verified = False
            poster = request.POST.get('edit-poster')
            property.poster = poster

            rent_cost = request.POST.get('edit-rent-cost')
            property.rent_cost = rent_cost
            size = request.POST.get('edit-size')
            property.size = size
            unit = request.POST.get('edit-unit')
            property.unit = unit
            # wished = "admin"
            zip_code = request.POST.get('edit-zip-code')
            property.zip_code = zip_code
            photo = request.FILES.get('edit-photo', None)
            if photo:
                property.photo = photo




            # Save to database
            property.save()

        messages.add_message(request, messages.INFO, "You successfully edit a property: %s" % property.house_name)
        print(property.house_name, "has been edited")
        return redirect("nova:property-detail", property.id)
    else:
        properties = Property.objects.all()
        for property in properties:
            if property.id == property_id:
                break
        return render(request, "nova/property/edit.html", {"property": property})


# Post comment for a property, using ajax for dynamics UIs, no need to refresh the page to see the new comment appended
def post_comment(request):
    print("This is post comment view")
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    print(request.POST)
    # print(request.body)
    if is_ajax and request.method == "POST":

        # property_id = request.POST.get('property-id')
        property_id = int(request.POST.get('property_id'))
        print(property_id)
        try:
            international_friendly = request.POST.get('international_friendly')
            comment_text = request.POST.get('comment_text')
            rating = request.POST.get('rating')
            finding_rm = request.POST.get('finding_rm')
            print(property_id)
            print(international_friendly)
            property = Property.objects.get(id=property_id)
            user = User.objects.get(username=request.session.get("username"))
            # poster = request.POST.get('poster')
            # Create a new comment instance
            comment = Comments(content=comment_text, international_friendly=international_friendly, property=property,
                               finding_rm=finding_rm, rating=rating, user=user)

            comment.save()

            action = Action(
                user=User.objects.get(username=request.session.get("username")),
                verb="posted a new review",
                target=comment.property
            )
            action.save()

            # Convert date type
            natural_time = timesince(comment.date_posted) + ' ago'

            # Json response including new comment information
            return JsonResponse(
                {'success': 'success', 'message': 'Comment added successfully.', 'comment_content': comment_text,
                 'comment_international_friendly': international_friendly,
                 'comment_rating': rating,
                 'comment_finding_rm': finding_rm, 'comment_poster': user.username, 'comment_id': comment.id,
                 'property_id': property_id, 'natural_time': natural_time}, status=200)

        except Property.DoesNotExist:

            return JsonResponse({'error': 'No property found with that ID'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request'}, status=400)


def delete_comment(request, property_id, comment_id):
    if not request.session.get('username', False):
        print("Please log in")
        return redirect('users:log-in-page')
    # elif not request.session['role'] == 'admin':
    #     print("Not admin or author, please log in")
    #     return redirect('nova:properties-list')
    else:
        # Fetch the property object or raise a 404 if not found
        comment_to_delete = Comments.objects.get(id=comment_id)
        comment_poster = comment_to_delete.user.username

        action = Action(
            user=User.objects.get(username=request.session.get("username")),
            verb="deleted the review",
            target=comment_to_delete.property
        )
        action.save()

        # Delete the property
        comment_to_delete.delete()

        print("Comment id", comment_id, "has been deleted")
        messages.add_message(request, messages.WARNING, "You deleted a comment posted by: %s" % comment_poster)

        return redirect("nova:property-detail", property_id)


# def delete_comment(request):
#
#     if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == "POST":
#         comment_id = request.POST.get('comment_id')
#         # print(comment_id)
#         # comment_id = int(comment_id)
#         try:
#             comment = Comments.objects.get(id=comment_id)
#             action = Action(
#                 user=User.objects.get(username=request.session.get("username")),
#                 verb="deleted the review",
#                 target=comment.property
#             )
#             action.save()
#             comment.delete()
#             return JsonResponse({'success': 'Comment deleted successfully'}, status=200)
#         except Comments.DoesNotExist:
#             return JsonResponse({'error': 'Comment not found'}, status=404)
#     else:
#         return JsonResponse({'error': 'Invalid Ajax request'}, status=400)


def edit_comment(request, property_id, comment_id):
    if not request.session.get('username', False):
        print("Please log in")
        return redirect('users:log-in-page')
    if request.method == 'POST':
        comments = Comments.objects.all()
        for comment in comments:
            if comment.id == comment_id:
                break

        # if not request.session.get('username', False):
        #     return redirect('users:log-in-page')
        if request.method == 'POST':
            print("Posting")
            # process the form
            # id
            international_friendly = request.POST.get('edit-international-friendly')
            comment.international_friendly = international_friendly
            comment_text = request.POST.get('edit-comment-text')
            comment.content = comment_text
            rating = int(request.POST.get('edit-rating'))
            comment.rating = rating
            finding_rm = request.POST.get('edit-finding-rm')
            comment.finding_rm = finding_rm
            comment.property = Property.objects.get(id=property_id)
            comment.user = User.objects.get(username=request.session.get("username"))
            # poster = request.POST.get('poster')
            # Create a new comment instance
            # comment = Comments(content=comment_text, international_friendly=international_friendly, property=property,
            #                    finding_rm=finding_rm, rating=rating, user=user)
            comment.save()

            action = Action(
                user=User.objects.get(username=request.session.get("username")),
                verb="edited the review",
                target=comment.property
            )
            action.save()

        messages.add_message(request, messages.INFO,
                             "You successfully edit a comment posted by: %s" % comment.user.username)
        print(comment.id, "comment has been edited")

        properties = Property.objects.all()
        for property in properties:
            if property.id == property_id:
                break
        return redirect("nova:property-detail", property.id)
    else:
        comments = Comments.objects.all()
        properties = Property.objects.all()
        for comment in comments:
            if comment.id == comment_id:
                break

        for property in properties:
            if property.id == property_id:
                break

        return render(request, "nova/property/comment-edit.html", {"comment": comment, "property": property})
    # return None
