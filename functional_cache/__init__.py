import sqlite3
from hashlib import sha1
from json import dumps as json_dumps


class FunctionalCache:
    def __init__(self, database_file=""):
        if database_file is "":
            conn = sqlite3.connect(":memory:")
        else:
            conn = sqlite3.connect(database_file)

        self.connection = conn
        try:
            self.create_tables()
        except sqlite3.OperationalError as e:
            if e.args[0] == 'table definition already exists':
                pass
            else:
                raise e

    def create_tables(self):
        self.connection.execute("create table definition("
                                "function_name, argument_hash,"
                                " arguments UNIQUE, return_value)")

    def print_tables(self):
        for row in self.connection.execute("select function_name, "
                                           "argument_hash, arguments,"
                                           " return_value from definition"):
            print(row)

    def add(self, function_name, args: tuple, kwargs, return_value):
        arg, hash_arg = self._make_args_and_hash(args, kwargs)
        values = [(function_name, hash_arg, arg, return_value)]
        try:
            self.connection.executemany(
                "insert into definition(function_name, argument_hash, "
                "arguments, return_value) values (?, ?, ?, ?)", values)
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get(self, function_name, args, kwargs):
        _, hash_arg = self._make_args_and_hash(args, kwargs)
        cur = self.connection.execute(
            ("select * from definition where "
             "function_name=:function_name and argument_hash=:arguments"), {
             "function_name": function_name, "arguments": hash_arg})
        output = cur.fetchall()
        if output:
            return output[0][-1]

    def apply_function(self, function, function_name, args, kwargs):
        return_value = self.get(function_name, args, kwargs)
        if return_value is None:
            # do function
            return_value = function(*args, **kwargs)
            self.add(function_name, args, kwargs, return_value)
            return return_value
        else:
            return return_value

    def cache(self, func):
        def wrapper(*args, **kwargs):
            return self.apply_function(func, func.__name__, args, kwargs)
        return wrapper

    @staticmethod
    def _make_args_and_hash(args, kwargs):
        arg = "+".join(str(x) for x in args)
        if kwargs:
            arg += "+" + json_dumps(kwargs, sort_keys=True,
                                    separators=(',', ':'))
        hash_arg = sha1(arg.encode()).hexdigest()
        return arg, hash_arg


SQLiteCache = FunctionalCache
