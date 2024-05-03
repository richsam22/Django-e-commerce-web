console.log("working fine");




$("#review-form").submit(function(e){
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function(response){
            console.log("comment save to Db.....");

            if(response.bool == true){
                $("#review-res").html("Review added successfully")
                $(".hide-comment-form").hide()

                let _html = '<div class="review">'
                    _html += '<div class="row no-gutters">'
                    _html += '<div class="col-auto">'
                    _html += '<h4><a href="#">"+ res.context.user +"</a></h4>'
                    
                    for(let i = 1; i < res.context.rating; i++ ){
                        _html += '<i class="fas fa-star text-warning>'
                    }

                    _html += '<p>{{ average_rating.rating|floatformat }} out of 5 p>'
                    _html += '<span class="review-date">{{ r.date|date:"d m,y"}} span>'
                    _html += '</div><!-- End .col -->'

                    _html += '<div class="col">'
                    _html += '<h4>Good, perfect size</h4>'

                    _html += '<div class="review-content">'
                    _html += '<p>"+ res.context.review +"</p>'
                    _html += '</div><!-- End .review-content -->'

                    _html += '<div class="review-action">'
                    _html += '<a href="#"><i class="icon-thumbs-up"></i>Helpful ( </a>'
                    _html += '<a href="#"><i class="icon-thumbs-down"> i>Unhelpful (0)    a>'
                    
                    _html += '</div><!-- End .review-action -->'
                    _html += '</div><!-- End .col-auto -->'
                    _html += '</div><!-- End .row -->'
                    $(".reviews").prepend(_html)
            }

        }
    })
})


// add to cart



$(".add-to-cart-btn").on("click", function(){
    
    let this_val = $(this)
    let index = this_val.attr("data-index")

    let quantity = $(".product-quantity-" + index).val()
    let product_title = $(".product-title-" + index).text()
    let product_id = $(".product-id-" + index).val()
    let product_price = $(".product-price-" + index).text()
    let product_pid = $(".product-pid-" + index).val()
    let product_image = $(".product-image-" + index).val()
    

    console.log("Quantity:", quantity);
    console.log("title:", product_title);
    console.log("price:", product_price);
    console.log("ID:", product_id);
    console.log("pid:", product_pid);
    console.log("image:", product_image);
    console.log("index:", index);
    console.log("Current Element:", this_val);


    $.ajax({
        url: '/add_to_cart',
        data: {
            "id": product_id,
            "qty": quantity,
            "title": product_title,
            "price": product_price,
            "pid": product_pid,
            "image": product_image,
        },
        dataType: 'json',
        beforeSend: function(){
            console.log("Adding Product to Cart...");

        },
        success: function(response){
            this_val.html('<i class="icon-check text-success"></i>')
            console.log("Product Added to Cart...");
            $(".cart-items-count").text(response.totalcartitems)


        }
    })
})

//    delete cart product

$(document).on("click", ".delete-product" ,function(){

    let product_id = $(this).attr("data-product")
    let this_val = $(this)

    console.log("Product ID:", product_id);


    $.ajax({
        url: '/delete_from_cart',
        data: {
            "id": product_id
            
        },
        dataType: 'json',
        beforeSend: function(){
            console.log("deleting from cart...")

        },
        success: function(response){
            this_val.show()
            $(".cart-items-count").text(response.totalcartitems)
            $("#cart-list").html(response.data)
            console.log("Deleted from cart")


        }
    })
})

//    update cart product

$(".update-product").on("click", function(){

    let product_id = $(this).attr("data-product")
    let this_val = $(this)
    let product_quantity = $(".product-qty-" + product_id).val()

    console.log("Product ID:", product_id);
    console.log("Product Qty:", product_quantity);


    $.ajax({
        url: '/update_cart',
        data: {
            "id": product_id,
            "qty": product_quantity,
            
        },
        dataType: 'json',
        beforeSend: function(){
            console.log("Updating cart...")

        },
        success: function(response){
            this_val.show()
            $(".cart-items-count").text(response.totalcartitems)
            $("#cart-list").html(response.data)
            console.log("Cart updated")


        }
    })
})

// making default address 

$(document).on("click", ".default-address", function(){
    let id = $(this).attr("data-address")
    let this_val = $(this)

    console.log("ID is:", id)
    console.log("Element is:", this_val)

    $.ajax({
        url: "/default-address",
        data: {
            "id": id
        },
        dataType: "json",
        success: function(response){
            console.log("Address Made Default....")
            if (response.boolean == true){

                $(".action_icon").hide()
                $(".action_btn").show()
                
                $(".check"+id).show()
                $(".button"+id).hide()
                
            }
        }

    })
})

// adding to wishlist

$(document).on("click", ".add-to-wishlist", function(){

    let product_id = $(this).attr("data-product-item")
    let this_val = $(this)

    console.log("Product ID is:", product_id);

    $.ajax({
        url: "/add-to-wishlist",
        data: {
            "id": product_id
        },
        dataType: "json",
        beforeSend: function(){
            console.log("Adding to Wishlist")
        },
        success: function(response){
            this_val.html('<i class="icon-check text-success"></i>')
            if (response.bool === true){
                console.log("Added to Wishlist...")
            }
        }
    })
})

// Remove from wislist

$(document).on("click", ".delete-wishlist-product", function(){
    let wishlist_id = $(this).attr("data-wishlist-product")
    let this_val = $(this)

    console.log("Wishlist ID is:", wishlist_id)

    $.ajax({
        url: "/remove-from-wishlist",
        data: {
            "id": wishlist_id,

        },
        dataType: "json",
        beforeSend: function(){
            console.log("Deleting product from wishlist...")
        },
        success: function(response){
            $("#wishlist-list").html(response.data)
            console.log("Deleted from wishlist")
            
        }
    })
})


// Contact form

$(document).on("submit", "#contact-form", function(e){
    e.preventDefault()
    console.log("Sumbited...")

    let full_name = $("#full_name").val()
    let email = $("#email").val()
    let phone = $("#phone").val()
    let subject = $("#subject").val()
    let message = $("#message").val()

    console.log("Full_name:", full_name)
    console.log("Email:", email)
    console.log("Phone:", phone)
    console.log("Subject:", subject)
    console.log("Message:", message)

    $.ajax({
        url: "/ajax-contact-form",
        data: {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "subject": subject,
            "message": message
        },
        dataType: "json",
        beforeSend: function(){
            console.log("Sending Data to Server...")
        },
        success: function(res){
            console.log("Data Successfully Sent.")
            $("#contact-form").hide()
            $("#message-response").html("Message Sent Sucessfully!")

        }

    })
})

// // add to cart

// $("#add-to-cart-btn").on("click", function(){
//     let quantity = $("#product-quantity").val()
//     let product_title = $("#product-title").text()
//     let product_id = $(".product-id").val()
//     let product_price = $(".product-price").text()
//     let this_val = $(this)

//     console.log("Quantity:", quantity);
//     console.log("title:", product_title);
//     console.log("price:", product_price);
//     console.log("ID:", product_id);
//     console.log("Current Element:", this_val);


//     $.ajax({
//         url: '/add-to-cart',
//         data: {
//             "id": product_id,
//             "qty": quantity,
//             "title": product_title,
//             "price": product_price,
//         },
//         dataType: 'json',
//         beforeSend: function(){
//             console.log("Adding Product to Cart...");

//         },
//         success: function(response){
//             this_val.html("Item Added to Cart.")
//             console.log("Product Added to Cart...");
//             $(".cart-items-count").text(response.totalcartitems)


//         }
//     })
// })