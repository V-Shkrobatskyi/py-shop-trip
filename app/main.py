import json
import math
import datetime
from typing import Union, Tuple

from app.car import Car
from app.customer import Customer
from app.shop import Shop


def shop_trip() -> None:
    with open("app/config.json", "r") as file:
        config_file = json.load(file)

    fuel_price = config_file["FUEL_PRICE"]
    customers = [
        Customer(
            customer["name"],
            customer["product_cart"],
            customer["location"],
            customer["money"],
            Car(
                customer["car"]["brand"],
                customer["car"]["fuel_consumption"],
            ),
        )
        for customer in config_file["customers"]
    ]
    shops = [
        Shop(
            shop["name"],
            shop["location"],
            shop["products"],
        )
        for shop in config_file["shops"]
    ]

    for customer in customers:
        print(f"{customer.name} has {customer.money} dollars")
        cheapest_prices: Tuple[Union[Shop | None], float | None] = (None, None)
        cheapest_shop_products = []
        for shop in shops:
            shop_dist = math.dist(customer.location, shop.location)
            cost_of_get_shop = (shop_dist * fuel_price
                                * customer.car.fuel_consumption / 100)
            shop_products = [
                [
                    product,
                    value,
                    value * shop.products[product]
                ]
                for product, value in customer.product_cart.items()
            ]
            cost_of_products = sum(shop_prod[2] for shop_prod in shop_products)
            final_price = round(cost_of_get_shop * 2 + cost_of_products, 2)
            print(f"{customer.name}'s trip to the "
                  f"{shop.name} costs {final_price}")
            if cheapest_prices[1] is None or cheapest_prices[1] > final_price:
                cheapest_prices = (shop, final_price)
                cheapest_shop_products = shop_products

        if cheapest_prices[1] <= customer.money:
            print(f"{customer.name} rides to {cheapest_prices[0].name}\n")
            date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"Date: {str(date_time)}\n"
                  f"Thanks, {customer.name}, for your purchase!\n"
                  f"You have bought: ")
            total_sum = 0
            for product in cheapest_shop_products:
                print(f"{product[1]} {product[0]}s for {product[2]} dollars")
                total_sum += product[2]
            print(f"Total cost is {total_sum} dollars\n"
                  f"See you again!\n\n"
                  f"{customer.name} rides home\n"
                  f"{customer.name} now has "
                  f"{round(customer.money - cheapest_prices[1], 2)} dollars\n")
        else:
            print(f"{customer.name} doesn't have enough money "
                  f"to make a purchase in any shop")


shop_trip()
