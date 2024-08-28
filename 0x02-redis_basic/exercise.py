#!/usr/bin/env python3
"""This module implements a redis task"""
import redis
import uuid
import functools
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """A decorator that counts the number of times a method is called."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for decorated function"""
        # Increment the count for this method
        key = method.__qualname__
        self._redis.incr(key)
        # Call the original method
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """The decorator stores the history of inputs and outputs for a method."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper for decorated function."""
        key = method.__qualname__
        # Store the inputs
        self._redis.rpush(f"{key}:inputs", str(args))
        # Call the original method and get the result
        result = method(self, *args, **kwargs)
        # Store the outputs
        self._redis.rpush(f"{key}:outputs", str(result))
        return result
    return wrapper


class Cache:
    def __init__(self):
        """
        Connects to the Redis server and initializes the cache object.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the provided data in the cache and returns a unique key.

        Args:
            data: The data to be stored (can be any type).

        Returns:
            A string representing the unique key assigned to the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key:
            str, fn: Optional[Callable] = None
            ) -> Optional[Union[str, int, float, bytes]]:
        """
        Retrieves the data stored at the specified key and applies the
        conversion function if provided.

        Args:
            key: The key of the data to retrieve.
            fn: An optional callable used to convert the data back to the
                desired format.

        Returns:
            The data stored at the key, converted if a conversion function is
            provided, or None if the key does not exist.
        """
        data = self._redis.get(key)
        if data is None:
            return None

        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves the data stored at the specified key and converts
        it to a string.

        Args:
            key: The key of the data to retrieve.

        Returns:
            The data stored at the key, converted to a string, or
            None if the key does not exist.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves the data stored at the specified key and converts
        it to an integer.

        Args:
            key: The key of the data to retrieve.

        Returns:
            The data stored at the key, converted to an integer, or
            None if the key does not exist.
        """
        return self.get(key, int)


def replay(method: Callable) -> None:
    """Displays the history of calls of a particular function."""
    self = method.__self__
    key = method.__qualname__
    call_count = self._redis.get(key).decode('utf-8')
    print(f"{key} was called {call_count} times:")
    inputs = self._redis.lrange(f"{key}:inputs", 0, -1)
    outputs = self._redis.lrange(f"{key}:outputs", 0, -1)
    for input_args, output in zip(inputs, outputs):
        args = input_args.decode('utf-8')
        result = output.decode('utf-8')
        print(f"{key}(*{args}) -> {result}")
