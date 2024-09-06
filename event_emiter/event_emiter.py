from functools import wraps

class EventEmitter:
    def __init__(self):
        self._listeners = {}

    def on(self, event_name):
        def decorator(func):
            if event_name not in self._listeners:
                self._listeners[event_name] = []
            self._listeners[event_name].append(func)

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def off(self, event_name):
        def decorator(func):
            if event_name in self._listeners:
                try:
                    self._listeners[event_name].remove(func)
                except ValueError:
                    print(f"Listener {func.__name__} is not registered for event '{event_name}'.")
            return func
        return decorator

    def emit(self, event_name, *args, **kwargs):
        listeners = self._listeners.get(event_name, [])
        for listener in listeners:
            listener(*args, **kwargs)
