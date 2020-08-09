'''
背景：在使用 Python 进行《我是动物饲养员》这个游戏的开发过程中，有一个代码片段要求定义动物园、动物、猫三个类。

这个类可以使用如下形式为动物园增加一只猫：
if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = getattr(z, 'Cat')

具体要求：
定义“动物”、“猫”、“动物园”三个类，动物类不允许被实例化。
动物类要求定义“类型”、“体型”、“性格”、“是否属于凶猛动物”四个属性，是否属于凶猛动物的判断标准是：“体型 >= 中等”并且是“食肉类型”同时“性格凶猛”。
猫类要求有“叫声”、“是否适合作为宠物”以及“名字”三个属性，其中“叫声”作为类属性，猫类继承自动物类。
动物园类要求有“名字”属性和“添加动物”的方法，“添加动物”方法要实现同一只动物（同一个动物实例）不能被重复添加的功能。
'''

from abc import ABCMeta, abstractmethod


class Animal(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, type, somatotype, character):
        self.type = type
        self.somatotype = somatotype
        self.character = character
        self.isViolent = False
        if (type == '食肉' and (somatotype == '大型' or somatotype == '中等') and character == '凶猛'):
            self.isViolent = True


class Cat(Animal):
    call = '喵呜'  

    def __init__(self, name, type, somatotype, character):
        self.name = name
        self.isPet = True
        super().__init__(type, somatotype, character)



class Zoo(object):
    def __init__(self, name): 
        self.name = name    
        self.animals = []

    def add_animal(self, instance):
        if instance in self.animals:
            print(f'{type(instance).__name__} existed')
        else:
            self.animals.append(instance)
            self.__dict__[type(instance).__name__] = instance
            print(f'{type(instance).__name__} add success')



if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = getattr(z, 'Cat') 
    have_cat = getattr(z, 'Dog')  