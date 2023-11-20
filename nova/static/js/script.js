$(document).ready(function () {

    // Show image description (how many people finding a roommate when mouse on the property picture
    showImageDescription();
    // Change the wish icon when the user click, and show the notification message
    toggleWishStatus();
    // Check query string
    checkQueryString();

    // nav, sorting tabs active
    activeNavElement();

    // Ajax for posting comments
    postComments();




});

// Ajax for post the comments
function postComments() {
    var ajax_url = $('#post-comment-input').attr('data-ajax-url');
    console.log('reach')
    console.log(ajax_url)
    // If the user click submit in the form
    $('#comment-form').on('submit', function (event) {
        event.preventDefault();  // Prevents the form from submitting in the traditional way

        // Read the submitted field
        var formData = {
            'rating': $('#rating').val(),
            'finding_rm': $('#add-finding-rm').val(),
            'international_friendly': $('#add-international-friendly').val(),
            'comment_text': $('textarea[name="comment-text"]').val(),
            'property_id': $('#property-id').val(),
            'poster': $('#comment-poster').val()
        };

        console.log(formData)
        console.log("ajaxurl", ajax_url)

        // Prepare ajax for POST
        $.ajax({
            url: ajax_url,
            type: 'POST',
            data: formData,
            dataType: 'json',
            context: this,
            headers: {"X-CSRFToken": csrftoken}


        }).done(function (json) {
            if (json.success === "success") {
                console.log("Request received successfully");

                // Create a new comment element
        let newComment = document.createElement("div");
        newComment.className = "review";

        let internationalFriendly = (json.comment_international_friendly) ? "Yes" : "No";
        let findingRm = (json.comment_finding_rm) ? "Yes" : "No";

        let urlContainer = document.getElementById('urlContainer');
                if (!urlContainer) {
                    urlContainer = document.createElement('div');
                    urlContainer.id = 'urlContainer';
                    urlContainer.dataset.profileUrl = "{% url 'users:profile' 'USERNAME' %}";
                    // Append it to the comments container or a suitable parent element
                    document.getElementById('commentsSection').appendChild(urlContainer);
    }

        const profileUrlTemplate = urlContainer.dataset.profileUrl;
        const profileUrl = profileUrlTemplate.replace('USERNAME', json.comment_poster);
   // <a href="#">${json.comment_poster}</a>
        newComment.innerHTML = ` 
             <a href="${profileUrl}">${json.comment_poster}</a>
             <h5 id="dateString">Date posted: ${json.natural_time}</h5>
            <img class="star" src="/static/img/star-solid.svg" alt="star"> ${json.comment_rating}
            <p>${json.comment_content}</p>
            <h4>International Friendly? ${internationalFriendly}</h4>
            <h4>Finding a roommate? ${findingRm}</h4>
<!--            <int:property_id>/comments/<int:comment_id>/edit-->
            <form class="delete-form" method="POST" action="${json.property_id}/comments/${json.comment_id}/delete">
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
                <input type="submit" class="delete-btn" value="Delete">
            </form>
            <a class="edit-link" href="${json.property_id}/comments/${json.comment_id}/edit">
                <button class="edit-btn">Edit</button>
            </a>
            <hr>
        `;

        // Append the new comment to the comments section
        // let commentsSection = document.getElementById("commentsSection");
        let commentsSection = document.getElementById("commentsSection");
        // Prepend the new comment
        commentsSection.innerHTML = newComment.innerHTML + commentsSection.innerHTML;
        // commentsSection.appendChild(newComment);
        //
        // // Add an HR
        // let hr = document.createElement("hr");
        // commentsSection.appendChild(hr);

        // Optional: Clear the comment input field if you have one
        $('#commentInputField').val('');

        console.log("Comment updated without refreshing the page")
            } else {
                console.log("Error: " + json.error)
            }

        }).fail(function (xhr, status, errorThrown) {
            console.log("Sorry, there was a problem!")
            console.log("Error: " + errorThrown);
        }).always(function (xhr, status) {
            console.log("The request is complete!");

        })

    })
}



function activeNavElement() {
    $(function ($) {
        var path = window.location.pathname;
        var sortParam = new URLSearchParams(window.location.search).get('sort');
        // var path = window.location.href; // 'href' property of the DOM element is the absolute path
        $('#primary-nav a').each(function () {
            if (this.pathname === path) {
                $(this).addClass('active');
            }else {
                $(this).removeClass('active'); // Optional: To ensure that previously highlighted links are deselected
            }
        });

        // Sorting active style
        if (!sortParam) {
            sortParam = 'availability'; // Set this to your default sorting option
        }

        $('a[href="?sort=' + sortParam + '"]').addClass('sort-active');

    });
}

// Search
// Retrieve the submitted keyphrase and to (using an if or switch statement))
// determine whether to display the simulated search results or the friendly error message.
// Keyword: wonderful
function checkQueryString() {
    var querystring = window.location.search;
    console.log(querystring);
    var urlParams = new URLSearchParams(querystring);
    if (urlParams.has('search-property')) {
        var keyword = urlParams.get("search-property");
        if (keyword == "wonderful") {
            // window.alert("You searched wonderful");
            // Hide the please search again message when it is matched, and show the property
            $('#search-failed-messages').css('display', 'none');
        } else {
            // window.alert("You did not search wonderful");
            // Hide the property when it is not matched, and show the please search again message
            $('#search-success').css('display', 'none');
        }
    }


}


// Show image description (how many people finding a roommate when mouse on the property picture
// Modifying an existing element (Picture), adding a new element (Image description on the top)
// Event delegation
function showImageDescription() {
    // Attach a delegated event handler for mouse entering the house images
    $("#properties").on("mouseenter", ".building-img", function () {
        // Change existing element: Applies graphical effects by changing opacity value
        $(this).css("filter", "opacity(0.5)");

        // Add new element: Show the image description below
        const description = $(this).data("description");
        $("#image-description").html(`<h3>${description}</h3>`);


    }).on("mouseleave", "img", function () {
        // Reset graphical effects when the mouse leaves
        $(this).css("filter", "opacity(1)");
    });

}

// Change wish icon status, and showing notification messages
// Modifying an existing element by changing the Wish icon, adding a new element (notification message if clicked under the corresponding property)
// DOM traversal
function toggleWishStatus() {
    // Event for clicking the wish icon button
    $(".wish-icon").click(function () {
        //     DOM traversal to find the parent div for each wish icon
        var $parentProperty = $(this).parent("div");
        console.log($(this).attr("src"));
        // If the icon is now heart-plus, change it to heart-minus, and append a message
        if ($(this).attr("src") === "/static/img/heart-plus.svg") {
            $(this).attr("src", "/static/img/heart-minus.svg");
            $parentProperty.append('<h4 class="wish-notification">Added to wishes!</h4>')
            // Otherwise,
        } else {
            $(this).attr('src', "/static/img/heart-plus.svg");
            // Using DOM traversal to find the correspond notification message and remove it
            $parentProperty.find(".wish-notification").remove();
            // Showing removed from wishes on the screen is a little bit unnecessary for the view of the website
            // $parentProperty.append('<h4 class="wish-notification">Removed from wishes!</h4>')

        }

    });

}

// For uploading image
function displayFileName() {
    const fileInput = document.getElementById('photo');
    const fileNameDisplay = document.getElementById('file-name');

    // Extract file name from the path (in case full path is given)
    const fileName = fileInput.value.split('\\').pop();

    // Display the file name
    fileNameDisplay.textContent = fileName ? `Selected: ${fileName}` : '';
}




// Used in ajax
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

