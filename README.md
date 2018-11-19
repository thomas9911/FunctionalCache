No depenencies, no external services functional cache.

Only relies on sqlite3 from the standard python library plus hashlib.sha1 and json.dumps also from standard library.


Note: Most of the limits are due to sqlite. There are other libraries who can relief you from these limits.
      Also this is probabily not usable as a 'real' cache because there is no 'expiry' option. That is why it is a functional cache:

`f(x) => y, where function f always gives output y given input x.`

Therefore it is usable for expensive and/or recursive functions.

### Example for a recursive factorial function:
```python
from functional_cache import FunctionalCache


f = FunctionalCache("factorial.db")


@f.cache
def factorial(n: int) -> str:
    """factorial function that returns the answer in a string.
    This so sqlite can save the large integers.
    """
    if n < 2:
        return "1"
    else:
        return str(n*int(factorial(n-1)))


def build_up_factorial(n):
    print("This will build a factorial database until {n}!".format(n=n))
    for i in range(20, n, 20):
        print("now at {i}".format(i=i), end="\r")
        factorial(i)


n = 900
build_up_factorial(n)
print("{}! = {}".format(n, factorial(n)))

```