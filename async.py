def final_callback():
    print('Complete! All functions were called!')

def error_callback(e):
    print('Error: ' + str(e) + '!')

class AsyncGroup:
    def __init__(self, final_callback, error_callback):
        self.wasError = False
        self.final_callback = final_callback
        self.error_callback = error_callback

    functions = []

    def add(self, func):
        self.functions.append(func)

        def innerFunc(*args):
            if self.wasError:
                return
            try:
                func(*args)
                self.functions.remove(func)
            except Exception as e:
                self.error_callback(e)
                self.wasError = True
            finally:
                if len(self.functions) == 0:
                    self.final_callback()

        return innerFunc

def func1(*args):
    print('Function 1 called! Args: ' + str(args[0]) + ' and ' + str(args[1]))
    a = args[0] / args[1]

def func2(*args):
    print('Function 2 called!')

def func3(*args):
    print('Function 3 called! Args: ' + str(args[0]))

group = AsyncGroup(final_callback, error_callback)

# It's ok
func11 = group.add(func1)
func12 = group.add(func2)
func13 = group.add(func3)

x, y, z = 5, 8, 9
func11(x, y)
func12()
func13(z)

print('\n');

# Something went wrong
func21 = group.add(func1)
func22 = group.add(func2)
func23 = group.add(func3)

x, y, z = 5, 0, 9
func21(x, y)
func22()
func23(z)