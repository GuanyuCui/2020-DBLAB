from django.test import TestCase

# Create your tests here.
class MyClass(object):
    def a(self):
        print('aaa')
        return self


    def b(self):
        print('bbb')
        return self


    def c(self):
        print('ccc')
        return self
obj = MyClass()
obj.a().b().c()
