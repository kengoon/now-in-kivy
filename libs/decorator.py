from kivy import platform


def silencer(func):
    class task:
        isSuccessful = lambda: True

    def dont_crash_task(*args, **kwargs):
        if platform == "android":
            func(*args, **kwargs)
        else:
            kwargs.get("callback")(task)

    return dont_crash_task


def android_only(func):
    def check_android(*args, **kwargs):
        if platform != "android":
            return
        func(*args, **kwargs)

    return check_android
