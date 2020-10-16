import functools

# TEMPLATE 1 - Decorator without argument
def my_decorator(func):
    @functools.wraps(func)
    def func_returning_func(*args, **kwargs):
        print("Before")
        func(*args, **kwargs)
        print("After")
    return func_returning_func

@my_decorator
def my_function():
    print('Hello')

# TEMPLATE 2 - Decorator with argument


def decorator_with_argument(num):
    def my_decorator(func):
        @functools.wraps(func)
        def func_returning_func(*arg, **kwargs):
            if num == 100:
                print("Not running function")
            else:
                func(*arg, **kwargs)
        return func_returning_func
    return my_decorator


token = 100
@decorator_with_argument(token)     # how to make token varies?
def my_function_2(x, y):
    return print(x + y)


my_function_2(4, 5)     # not working because token == 100

token = 111
my_function_2(4, 5)     # not working because token has been 100 when initializing?

# def sum_decorator_with_argument(num):
def sum_decorator(func):
    def func_returning_func(*arg, **kwargs):     # always add *arg and **kwargs
        return 2 * func(*arg, **kwargs)
    return func_returning_func
    # return sum_decorator


# @sum_decorator
def sum(x, y, z):
    return x + y + z

print(sum_decorator(sum)(1,2,3))

