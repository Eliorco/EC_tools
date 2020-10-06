"""
Every code need optimization, this tool show you the runtime of your function only add @timeit decorator
"""
import time
import logging
import os
import timeit

def avg_timer(number, repeat):
    def wrapper(func):
        runs = timeit.repeat(func, number=number, repeat=repeat)
        print(f'Runtime took: {float(sum(runs)/ len(runs)):0.2f}')

    return wrapper

def func_timeit(method):
    logger = logging.getLogger()
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
            logger.info(f"function: '{name}', accumulative time is: '{kw['log_time'][name]}'")
        else:
            print('{0}  {1} ms'.format(method.__name__, (te - ts) * 1000))
            logger.info(f"func: '{method.__name__}', time: '{(te - ts) * 1000:2.2f}'")
        return result

    return timed


if __name__ == '__main__':

    #timeit logger
    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename=os.path.abspath(os.path.join(os.getcwd(),"..", "logs", f"timeit_{int(time.time())}.log")),
                        level=logging.DEBUG,
                        format=LOG_FORMAT)
    logger = logging.getLogger()

    # timeit POC
    @func_timeit
    def npow2():
        a = 0
        for i in range(100):
            for j in range(100):
                a = i + j + a

        return a


    @func_timeit
    def npow2_gen():
        a = 0
        x = (i for i in range(100))
        for j in range(100):
            a = next(x) + j + a

        return a

    npow2()
    npow2_gen()
