"""
some useful functions that are convenient to have so they don't have to be
defined in several files
"""

def drange(start, stop, step=1):
    """
    generator that returns an iterator between start and stop with any step value
    (not just an int). Similar in functionality to np.linspace(start, stop, num=(stop-start)/step)
    except it's an iterator so it doesn't return an np.array and it saves memory.
    """
    yield start;
    if step > 0:
        while (start + step) < stop:
            start += step;
            yield round(start, 2);
    else:
        while (start + step) > stop:
            start += step;
            yield round(start, 2);
