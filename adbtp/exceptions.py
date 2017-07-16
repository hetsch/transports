"""
    adbtp.exceptions
    ~~~~~~~~~~~~~~~~

    Contains exception types used across the package.
"""
import functools

from . import hints


class TransportProtocolError(Exception):
    """
    Base exception for all transport protocol related errors.
    """


class TransportTimeoutError(TransportProtocolError):
    """
    Exception raised when a transport action exceeds the specified timeout.
    """


class TransportClosedError(TransportProtocolError):
    """
    Exception raised when attempting to perform an action of a closed transport.
    """


def reraise(exc_to_catch: hints.ExceptionTypes):
    """
    Decorator that catches specific exception types and re-raises them as
    :class:`~adbtp.exceptions.TransportProtocolError`.

    :param exc_to_catch: Transport specific timeout exception type(s) to catch
    :type exc_to_catch: :class:`~Exception` or :class:`~tuple`
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exc_to_catch as e:
                raise TransportProtocolError('Transport encountered an error') from e
        return wrapper
    return decorator


def reraise_timeout_errors(exc_to_catch: hints.ExceptionTypes):
    """
    Decorator that catches transport specific timeout related exceptions to re-raise another.

    :param exc_to_catch: Transport specific timeout exception type(s) to catch
    :type exc_to_catch: :class:`~Exception` or :class:`~tuple`
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exc_to_catch as e:
                raise TransportTimeoutError(
                    'Exceeded timeout of {} ms'.format(kwargs.get('timeout', 'inf'))) from e
        return wrapper
    return decorator