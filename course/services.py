import stripe


def conver_currensies(price, name_course):
    usd_price = 100
    product = stripe.Product.create(name=name_course)
    price = stripe.Price.create(
        unit_amount=price * usd_price,
        currency="usd",
        product=product.id
    )
    success = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[
            {
                "price": price.id,
                "quantity": 1,
            },
        ],
        mode="payment",
    )
    return success.url





    #responce = requests.get(
        #"sk_test_51O5OaREACBiS2uPOBXY2YGEER0cfdGQl90CqKxJ7aygxvkLMYVwmu0GAikXhMdcO7Vd0mdiMF1usTv2CR4TuHXbD00V6Ixpw6P"
    # if responce.status_code == status.HTTP_200_OK:
    #     usd_rate = responce.json()['data']['RUB']['value']
    #     usd_price = rub_price * usd_rate
    # return usd_price