
def hello(y, x, z=1, **kwargs):
    """
    description function hello
    """
    print('hello')
    print(kwargs)
    return x + 2 * y + 3 * z


def bonjour(x):
    """
    description function bonjour
    """
    print('bonjour')
    return x


class Hallo():
    """
    description class Hallo
    """

    def __init__(self, name):
        self.name = name
        self.polite('!')

    def __repr__(self):
        return 'My name is ' + self.name

    def polite(self, name, n=3, **kwargs):
        """
        description method polite
        """
        print('n={}'.format(n))
        self.sentence = 'Hallo {} ({} times)'.format(self.name, n)
        return 'Welcome to my hotel, Mr ' + str(name)

    def test(self):
        """
        description method test
        """
        return 'testing: ' + self.name
