class Duck:
    def __init__(self, obj):
        self._obj = obj

    def attr(self, *items, **kw):
        for attr_name in items:
            try:
                return getattr(self._obj, attr_name)
            except AttributeError:
                pass

        e = AttributeError("None of given attributes found in %r" % self._obj)
        return self._default_or_raise(e, kw)

    def attr_call(self, *duck_ctxs, **kw):
        last_err = None
        for ctx in duck_ctxs:
            try:
                if isinstance(ctx, str):
                    return getattr(self._obj, ctx)
                else:
                    return ctx(self._obj)
            except (AttributeError, TypeError) as e:
                last_err = e
        return self._default_or_raise(last_err, kw)

    def __call__(self, *args, **kw):
        for arg in args:
            duck_call = DuckCall("__call__", *arg)
            try:
                return duck_call(self._obj)
            except TypeError as e:
                last_err = e
        return self._default_or_raise(last_err, kw)

    def _default_or_raise(self, e, kw):
        if "default" in kw:
            return kw["default"]
        raise e


class DuckCall:
    def __init__(self, name, args=None, kwargs=None):
        self._name = name
        self._args = args or []
        self._kwargs = kwargs or {}

    def __call__(self, obj):
        return getattr(obj, self._name)(*self._args, **self._kwargs)


class DuckGet:
    def __init__(self, name):
        self._name = name

    def __call__(self, obj):
        return getattr(obj, self._name)
