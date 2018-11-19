import time
from functional_cache import FunctionalCache


f = FunctionalCache("factorial.db")
# s = FunctionalCache()


@f.cache
def sleep_tests(a, b):
    time.sleep(2)
    return a**2 + b


@f.cache
def sleep_tests2(x, y, z):
    time.sleep(2)
    return (x+y)**(2*z)


@f.cache
def factorial(n: int) -> str:
    """factorial function that returns the answer in a string.
    This so sqlite can save the large integers.
    """
    if n < 2:
        return "1"
    else:
        return str(n*int(factorial(n-1)))


@f.cache
def keyword_test(a, b=None):
    return a


# print(sleep_tests(1,2))
# print(sleep_tests(1,2))
# print(sleep_tests2(1, 2, 2))
# print(sleep_tests(1,2))
# print(sleep_tests(1,2))
# print(sleep_tests(1,2))


# print(factorial(900))
# print(keyword_test(a=5, b={"derp": 14}))
# s.print_tables()


def build_up_factorial(n):
    print("This will build a factorial database until {n}!".format(n=n))
    for i in range(20, n, 20):
        print("now at {i}".format(i=i), end="\r")
        factorial(i)

n = 900
build_up_factorial(n)
print("{}! = {}".format(n, factorial(900)))
