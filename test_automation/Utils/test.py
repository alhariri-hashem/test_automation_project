from test_automation.Utils.menu import Menu
from test_automation.Utils.menu_item import MenuItem


# navigation = OrderedDict({'h': 'home', 'e': 'exit'})
# m = ChainMap(navigation)
# main_menu = OrderedDict({'1': 'add a comment', '2': 'take a screenshot'})
# add_a_comment_sub = OrderedDict({'1': 'add a comment1', 'y': 'add another'})
# m = m.new_child(main_menu)
# print(m['h'])
# print(m['1'])
# m = m.new_child(add_a_comment_sub)
# print(m['h'])
# print(m['1'])
# m = m.parents
# print(m['h'])
# print(m['1'])
# print(m)


@MenuItem(option='o', name='add a comment')
def add_a_comment():
    comment = input("please enter a comment?")
    print("OK. Noted ")


m = Menu()
m.add(add_a_comment)
m.show()
m['o'].action()
