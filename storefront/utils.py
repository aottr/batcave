from storefront.models import Product, CartItem, ProductSize, ProductColor


def check_stock(product: Product, size, color, amount):

    if product.stock_selector == product.StockChoices.PRODUCT:
        return product.stock >= amount
    elif product.stock_selector == product.StockChoices.SIZE:
        return size.stock >= amount
    elif product.stock_selector == product.StockChoices.COLOR:
        print(color.stock)
        print(amount)
        print(color.stock >= amount)
        return color.stock >= amount

    return False


def calculate_stock(cart_item: CartItem, add_to_cart=True):
    product = cart_item.item.product
    if product.stock_selector == product.StockChoices.PRODUCT:
        product.stock = product.stock - cart_item.amount if add_to_cart else product.stock + cart_item.amount
        product.save()
    elif product.stock_selector == product.StockChoices.SIZE:
        if add_to_cart:
            cart_item.item.size.stock -= cart_item.amount
        else:
            cart_item.item.size.stock += cart_item.amount
        cart_item.item.size.save()
    elif product.stock_selector == product.StockChoices.COLOR:
        if add_to_cart:
            cart_item.item.color.stock -= cart_item.amount
        else:
            cart_item.item.color.stock += cart_item.amount
        cart_item.item.color.save()
