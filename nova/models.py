from django.db import models
from datetime import datetime

# Create your models here.
# Main item property
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Property(models.Model):
    house_name = models.CharField(max_length=200)
    # house_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.IntegerField(default=0)
    address = models.CharField(max_length=200)
    unit = models.IntegerField(default=0)
    floor = models.IntegerField(default=0)
    bedrooms_count = models.IntegerField(default=0)
    bathrooms_count = models.IntegerField(default=0)
    rent_cost = models.IntegerField(default=0)
    size = models.IntegerField(default=0)
    initial_fee = models.IntegerField(default=0)
    availability = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='houses/')
    description = models.TextField(max_length=2000)
    date_posted = models.DateTimeField(auto_now_add=True)
    # rating = models.FloatField(default=0.0)
    is_verified = models.BooleanField(default=False)
    finding_rm = models.IntegerField(default=0)
    poster = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # wished = models.CharField(max_length=50)
    def __str__(self):
        return self.house_name

    def get_absolute_url(self):
        return reverse('nova:property-detail', args=[self.id])
        # path('<int:property_id>', views.property_detail, name="property-detail"),


class Comments(models.Model):
    property = models.ForeignKey(Property, related_name='comments', on_delete=models.CASCADE)
    poster = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    international_friendly = models.BooleanField(default=True)
    content = models.TextField(max_length=500)
    rating = models.IntegerField(default=0)
    finding_rm = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.property.house_name

    def get_absolute_url(self):
        return reverse('nova:property-detail', args=[self.property.id])
# class Property:
#     def __init__(self, id, house_name, city, zip_code, address, unit,
#                  floor, bedrooms_count, bathrooms_count, rent_cost, size,
#                  initial_fee, availability, description, date_posted, rating, is_verified, photo, finding_rm, comments,
#                  poster, wished):
#         self.id = id
#         self.house_name = house_name
#         self.city = city
#         self.zip_code = zip_code
#         self.address = address
#         self.unit = unit
#         self.floor = floor
#         self.bedrooms_count = bedrooms_count
#         self.bathrooms_count = bathrooms_count
#         self.rent_cost = rent_cost
#         self.size = size
#         self.initial_fee = initial_fee
#         self.availability = availability
#         self.photo = photo
#         self.description = description
#         self.date_posted = date_posted
#         self.rating = rating
#         self.is_verified = is_verified
#         self.finding_rm = finding_rm
#         # self.url = url
#         self.comments = comments
#         self.poster = poster
#         self.wished = wished

# # Sub item comments, inside each property
# class Comments:
#     def __init__(self, id, poster, rating, international_friendly, finding_rm, content
#                  ):
#         self.id = id
#         self.poster = poster
#         self.international_friendly = international_friendly
#         self.content = content
#         self.rating = rating
#         self.finding_rm = finding_rm

# # Creat sub items
# comment1 = Comments(
#     id=1,
#     poster="Lisa",
#     rating=4.0,
#     international_friendly=True,
#     finding_rm=True,
#     content="I recently stayed at “Wonderful Land” located at 7575 Cherries Rd., Tysons, VA, and it was a delightful "
#             "experience overall. The apartment, priced at $2000/month, offers 2 spacious bedrooms and a bathroom, "
#             "sprawling across 950 sq ft. While I appreciated the size and layout of the place, I found that the "
#             "bathroom could use a bit of modernization to enhance the overall living experience. Nevertheless, "
#             "the location is fantastic, providing easy access to various amenities in Tysons, making it a convenient "
#             "choice despite minor shortcomings."
#
# )
#
#
# # Creating main items
# property1 = Property(
#     1,
#     "Wonderful Land",
#     "Tysons",
#     22181,
#     "7575, Cherries Rd., Tysons, VA 22181",
#     213,
#     2,
#     2,
#     1,
#     2000,
#     950,
#     1200,
#     True,
#     "Unveiling Wonderful Land, a realm of comfort and convenience nestled at 7575 Cherries Rd., Tysons, VA. Priced at "
#     "a modest $2000/month, this residence opens the doors to a living space where every detail is a testament to "
#     "quality and care. Enclosed within its warm embrace are rooms that speak the language of comfort, ensuring each "
#     "day you spend is wrapped in coziness. Its prime location in Tysons is a gateway to a multitude of amenities, "
#     "simplifying your daily life with easy access to what the vibrant city has to offer. However, a word of caution "
#     "for our international friends – the community may require some time to adapt to diverse international needs and "
#     "expectations. Despite this, Wonderful Land stands as a beacon of comfort and convenience, making it a worthy "
#     "consideration for your new home. 🏡✨",
#     datetime.now(),
#     4.2,
#     True,
#     "img/houses/wonderful-land-tysons-building.jpg",
#     10,
#     # "detail.html",
#     comments=[comment1, comment2],
#     poster="rich",
#     wished='admin'
#
# )

# comment2 = Comments(
#     id=2,
#     poster="Keyboard_man",
#     rating=4.0,
#     international_friendly=True,
#     finding_rm=True,
#     content="“Wonderful Land” at 7575 Cherries Rd., Tysons, VA, is generally a comfortable and spacious option with "
#             "its 2 bedrooms and 950 sq ft of space at a rate of $2000/month. The location is ideal, situated close to "
#             "various amenities and the vibrancy of Tysons. However, a drawback is the limited parking availability "
#             "which can be somewhat inconvenient at times. Despite this, the apartment’s interiors and community feel "
#             "make it a good consideration for potential renters."
#
# )
#
# comment3 = Comments(
#     id=3,
#     poster="Handsome Tom",
#     rating=5.0,
#     international_friendly=True,
#     finding_rm=True,
#     content="As an international student, I found this Vienna, VA apartment to be a perfect blend of comfort and "
#             "convenience. The sunny 800 sq ft space and friendly community made my transition to the US seamless. "
#             "Highly recommend for students seeking a prime location at a reasonable price!"
#
# )
#
# comment4 = Comments(
#     id=4,
#     poster="Cool John",
#     rating=3.5,
#     international_friendly=True,
#     finding_rm=False,
#     content="While this apartment offers a convenient location and a spacious 800 sq ft layout ideal for "
#             "international students, I did notice the kitchen could use some updates. Nonetheless, the friendly "
#             "community and affordable rent made my stay worthwhile. A good option for students, but be prepared for a "
#             "bit of a DIY spirit in the kitchen!"
#
# )
#
# comment5 = Comments(
#     id=5,
#     poster="Mouse man",
#     rating=3.0,
#     international_friendly=True,
#     finding_rm=False,
#     content="Comfort Fairfax located at 5566 Blueberry St., Fairfax, VA, is a residence that truly lives up to its "
#             "name. Priced at $2300/month, the home offers a blend of comfort and convenience that is ideal for anyone "
#             "looking to experience the best of Fairfax. However, it is worth noting that the exterior lighting could "
#             "be improved for better visibility and safety during nighttime. Overall, the property maintains a high "
#             "standard of living, making it a worthy consideration despite minor areas for improvement."
# )
#
# comment6 = Comments(
#     id=6,
#     poster="Paddy Lewis",
#     rating=5.0,
#     international_friendly=True,
#     finding_rm=False,
#     content="Arlington Paradise at 3333 Pumpkin St., Arlington, VA, offers a lovely living experience with its 2 "
#             "bedrooms and 990 sq ft of space for $3000/month. The residence enjoys a prime location in Arlington, "
#             "ensuring easy access to local amenities and conveniences. However, a slight downside is the property's "
#             "proximity to a busy street, which occasionally brings in traffic noise. Despite this, the apartment's "
#             "interior is well-maintained and charming, making it a strong contender for anyone seeking quality "
#             "accommodation in Arlington."
# )
#
# comment7 = Comments(
#     id=7,
#     poster="TonLingAr",
#     rating=4.0,
#     international_friendly=True,
#     finding_rm=True,
#     content="This property is a delightful find, offering a generous 990 sq ft with 2 comfortable bedrooms for "
#             "$3000/month. Positioned in a vibrant Arlington neighborhood, the residence is close to various amenities "
#             "and services. However, prospective tenants should be mindful of the limited storage space available, "
#             "which might require some creative organization. Nevertheless, its fantastic location and the overall "
#             "comfort and design of the home offer a wonderful living experience."
# )
#
# comment8 = Comments(
#     id=8,
#     poster="Windows_Mac",
#     rating=3.0,
#     international_friendly=False,
#     finding_rm=False,
#     content="The apartment is situated in a lively neighborhood with easy access to various amenities. However, "
#             "it seems that the community is not as welcoming to international students, which can make the adjustment "
#             "process a bit challenging. Despite this, the apartment itself is quite comfortable and spacious, "
#             "but a more inclusive community spirit would enhance the overall living experience."
# )

#
# property2 = Property(
#     2,
#     "The Best Resort",
#     "Vienna",
#     22180,
#     "8989, Avocado Rd., Vienna, VA 22180",
#     311,
#     3,
#     2,
#     1,
#     1200,
#     800,
#     1000,
#     True,
#     "Cozy 1BR/1BA Apartment in Vienna, VA – Perfect for International Students! Situated in the heart of Vienna, VA, "
#     "this apartment offers a harmonious blend of convenience and charm. Surrounded by local cafes, parks, "
#     "and cultural sites, you'll be part of a vibrant community. We understand the unique needs of international "
#     "students and aim to make your transition smooth. This space is designed to be your home away from home. The "
#     "apartment boasts a modern kitchen, spacious living room, and ample storage. Natural light floods the living "
#     "areas, making for a warm and inviting atmosphere.",
#     datetime.now(),
#     4.5,
#     True,
#     "img/houses/the-best-resort-falls-church-building.jpg",
#     6,
#     # "detail.html",
#     comments=[comment3, comment4],
#     poster="admin",
#     wished='rich'
#
# )
#
# property3 = Property(
#     3,
#     "Comfort Fairfax",
#     "Fairfax",
#     22123,
#     "5566 Blueberry St., Fairfax, VA 22123",
#     605,
#     6,
#     2,
#     2,
#     2300,
#     980,
#     1800,
#     False,
#     "Experience the comfort and ease of living at Comfort Fairfax, located at 5566 Blueberry St. For $2300/month, "
#     "indulge in a residence that effortlessly combines convenience and style. Ideally situated in Fairfax, VA, "
#     "this home ensures that you are closely connected to a multitude of amenities, enhancing your daily living "
#     "experience. Please note that while the property has much to offer, international students may find the community "
#     "atmosphere to be less accommodating. Choose Comfort Fairfax for a thoughtful blend of location and design in "
#     "your new home. 🏡🌆",
#     datetime.now(),
#     4.5,
#     True,
#     "img/houses/comfort-apartment-fairfax.jpg",
#     3,
#     # "detail.html",
#     comments=[comment5],
#     poster="rich",
#     wished='admin'
#
# )
#
# property4 = Property(
#     4,
#     "Arlington Paradise",
#     "Arlington",
#     22204,
#     "3333 Pumpkin St., Arlington, VA 22204",
#     901,
#     9,
#     2,
#     1,
#     3000,
#     990,
#     2000,
#     False,
#     "Discover Arlington Paradise at 3333 Pumpkin St., a spacious 2-bedroom, 1-bathroom apartment offering 990 sq ft "
#     "of comfortable living space for $3000/month. Nestled in a vibrant Arlington neighborhood, this residence "
#     "provides easy access to an array of local amenities, ensuring utmost convenience. While beautifully designed "
#     "interiors promise a luxurious living experience, please note that the community might not be as welcoming to "
#     "international students. Choose Arlington Paradise for a home that blends style, comfort, and convenience. 🌿🏠",
#     datetime.now(),
#     4.9,
#     True,
#     "img/houses/arlington-paradise.jpg",
#     12,
#     # "detail.html",
#     comments=[comment6, comment7, comment8],
#     poster="admin",
#     wished='rich'
#
# )
#
# # Add each item into a list
# properties = []
# properties.append(property1)
# properties.append(property2)
# properties.append(property3)
# properties.append(property4)


# User credentials, one for regular user, one for admin user
regular_user = {"username": "rich",
                "password": "regular"
                }

admin_user = {
    "username": "admin",
    "password": "admin"
}
