from datetime import datetime

# Lớp Người Dùng
class User:
    def __init__(self, name, address):
        self.name = name
        self.address = address

# Lớp Khách Hàng kế thừa từ lớp Người Dùng
class Customer(User):
    def __init__(self, name, address, email, password):
        super().__init__(name, address)
        self.email = email
        self.password = password
        self.balance = 0

# Lớp Quản Lý kế thừa từ lớp Người Dùng
class Manager(User):
    def __init__(self, name, address):
        super().__init__(name, address)

# Lớp Món Ăn
class Dish:
    def __init__(self, name, price=500000):
        self.name = name
        self.price = price

class NB(Dish):
    def __init__(self, name):
        super().__init__(name)

# Lớp Giỏ Hàng
class Cart:
    def __init__(self, customer):
        self.customer = customer
        self.items = {}

    def add_item(self, dish, quantity):
        if dish.name in self.items:
            self.items[dish.name] += quantity
        else:
            self.items[dish.name] = quantity

    def remove_item(self, dish, quantity):
        if dish.name in self.items:
            if self.items[dish.name] <= quantity:
                del self.items[dish.name]
            else:
                self.items[dish.name] -= quantity

    def total_price(self):
        total = 0
        for item, quantity in self.items.items():
            total += quantity * 500000
        return total

# Lớp Đơn Đặt Hàng
class Order:
    def __init__(self, customer, cart):
        self.customer = customer
        self.cart = cart
        self.order_date = datetime.now()
        self.delivery_date = None

    def set_delivery_date(self, delivery_date):
        self.delivery_date = delivery_date

    def display_order(self):
        print(f"Customer: {self.customer.name}")
        print(f"Order Date: {self.order_date}")
        print(f"Delivery Date: {self.delivery_date}")
        print("Items:")
        for item, quantity in self.cart.items.items():
            print(f"{item}: {quantity} x 500000 = {quantity * 500000}")
        print(f"Total Price: {self.cart.total_price()}")

# Lớp Thông Tin Vận Chuyển
class ShippingInfo:
    SHIPPING_FEES = {
        'Xe máy': 5000,
        'Ô tô': 10000,
        'Máy bay': 15000
    }

    def __init__(self, order, shipping_method):
        self.order = order
        self.shipping_method = shipping_method
        self.shipping_fee = self.SHIPPING_FEES.get(shipping_method, 0)

    def display_shipping_info(self):
        self.order.display_order()
        print(f"Shipping Method: {self.shipping_method}")
        print(f"Shipping Fee: {self.shipping_fee}")

# Lớp QuanLyShop
class QuanLyShop:
    def __init__(self):
        self.menu = [
            NB('Dango'), NB('Bánh Dorayaki'), NB('Cơm trứng cuộn Omurice'),
            NB('Mì Udon'), NB('Cơm lươn nướng Unadon'), NB('Lẩu Sukiyaki'),
            NB('Mì Ramen'), NB('Mì Soba'), NB('Thịt nướng Yakiniku'), 
            NB('Súp miso'), NB('Cơm cà ri'), NB('Natto'), NB('Lẩu shabu-shabu'),
            NB('Takoyaki')
        ]
        self.orders = []
        self.shipping_infos = []

    def add_dish(self, dish):
        self.menu.append(dish)

    def remove_dish(self, dish_name):
        self.menu = [dish for dish in self.menu if dish.name != dish_name]

    def display_menu(self):
        for dish in self.menu:
            print(f"  - {dish.name}: {dish.price}")

    def create_order(self, customer, cart):
        order = Order(customer, cart)
        self.orders.append(order)
        return order

    def display_orders(self):
        for order in self.orders:
            order.display_order()

    def total_revenue(self):
        return sum(order.cart.total_price() for order in self.orders) + sum(shipping_info.shipping_fee for shipping_info in self.shipping_infos)

    def add_shipping_info(self, shipping_info):
        self.shipping_infos.append(shipping_info)

def main():
    quanlyshop = QuanLyShop()
    customer = None
    cart = None

    while True:
        print("\n=== Quản lý Cửa Hàng Ẩm Thực VJU-SHOP ===")
        print("1. Đăng ký khách hàng")
        print("2. Thêm món ăn vào giỏ hàng")
        print("3. Xóa món ăn khỏi giỏ hàng")
        print("4. Tạo đơn đặt hàng")
        print("5. Hiển thị menu")
        print("6. Hiển thị đơn hàng")
        print("7. Hiển thị tổng chi phí")
        print("8. Tạo thông tin vận chuyển")
        print("9. Hiển thị thông tin vận chuyển")
        print("10. Xác nhận đặt hàng")
        print("11. Thoát")
        choice = input("Chọn một tùy chọn: ")

        if choice == "1":
            name = input("Nhập tên khách hàng: ")
            address = input("Nhập địa chỉ: ")
            email = input("Nhập email: ")
            password = input("Nhập mật khẩu: ")
            customer = Customer(name, address, email, password)
            cart = Cart(customer)
            print("Khách hàng đã được đăng ký thành công!")

        elif choice == "2":
            if customer is None:
                print("Vui lòng đăng ký khách hàng trước.")
                continue
            quanlyshop.display_menu()
            dish_name = input("Nhập tên món ăn: ")
            quantity = int(input("Nhập số lượng: "))
            found = False
            for dish in quanlyshop.menu:
                if dish.name == dish_name:
                    cart.add_item(dish, quantity)
                    print(f"{quantity} {dish_name} đã được thêm vào giỏ hàng.")
                    found = True
                    break
            if not found:
                print("Món ăn không tồn tại.")

        elif choice == "3":
            if customer is None:
                print("Vui lòng đăng ký khách hàng trước.")
                continue
            dish_name = input("Nhập tên món ăn cần xóa: ")
            quantity = int(input("Nhập số lượng cần xóa: "))
            found = False
            for dish in quanlyshop.menu:
                if dish.name == dish_name:
                    cart.remove_item(dish, quantity)
                    print(f"{quantity} {dish_name} đã được xóa khỏi giỏ hàng.")
                    found = True
                    break
            if not found:
                print("Món ăn không tồn tại.")

        elif choice == "4":
            if customer is None:
                print("Vui lòng đăng ký khách hàng trước.")
                continue
            if not cart.items:
                print("Giỏ hàng đang trống.")
                continue
            order = quanlyshop.create_order(customer, cart)
            delivery_date = input("Nhập ngày giao hàng (YYYY-MM-DD): ")
            order.set_delivery_date(datetime.strptime(delivery_date, "%Y-%m-%d"))
            print("Đơn đặt hàng đã được tạo thành công!")
            cart = Cart(customer)  # Tạo giỏ hàng mới cho lần mua tiếp theo

        elif choice == "5":
            quanlyshop.display_menu()

        elif choice == "6":
            quanlyshop.display_orders()

        elif choice == "7":
            print(f"Tổng chi phí: {quanlyshop.total_revenue()}")

        elif choice == "8":
            if not quanlyshop.orders:
                print("Không có đơn đặt hàng để tạo thông tin vận chuyển.")
                continue
            order_index = int(input("Nhập chỉ số đơn hàng để tạo thông tin vận chuyển: ")) - 1
            if order_index < 0 or order_index >= len(quanlyshop.orders):
                print("Chỉ số đơn hàng không hợp lệ.")
                continue
            order = quanlyshop.orders[order_index]
            print("Chọn hình thức vận chuyển:")
            print("1. Xe máy (5k)")
            print("2. Ô tô (10k)")
            print("3. Máy bay (15k)")
            shipping_choice = input("Nhập lựa chọn của bạn: ")

            if shipping_choice == "1":
                shipping_method = "Xe máy"
            elif shipping_choice == "2":
                shipping_method = "Ô tô"
            elif shipping_choice == "3":
                shipping_method = "Máy bay"
            else:
                print("Lựa chọn không hợp lệ.")
                continue

            shipping_info = ShippingInfo(order, shipping_method)
            quanlyshop.add_shipping_info(shipping_info)
            print("Thông tin vận chuyển đã được tạo thành công!")

        elif choice == "9":
            if not quanlyshop.shipping_infos:
                print("Không có thông tin vận chuyển để hiển thị.")
                continue
            shipping_index = int(input("Nhập chỉ số thông tin vận chuyển để hiển thị: ")) - 1
            if shipping_index < 0 or shipping_index >= len(quanlyshop.shipping_infos):
                print("Chỉ số thông tin vận chuyển không hợp lệ.")
                continue
            shipping_info = quanlyshop.shipping_infos[shipping_index]
            shipping_info.display_shipping_info()
        
        elif choice == "10":
            print("Xác nhận đặt hàng thành công.")
        
        elif choice == "11":
            print("Thoát khỏi chương trình.")
            break

        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

if __name__ == "__main__":
    main()
