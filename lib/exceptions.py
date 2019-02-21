import functools
import logging
def exception(logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                logger.setLevel(logging.INFO)
                print (args)
                logger.info('Entering func')
                return  func(*args,**kwargs)
            except:
                err += func.__name__
                logger.exception(err)
            raise
        return wrapper
    return decorator
