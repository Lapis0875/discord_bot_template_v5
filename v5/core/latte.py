from .v5 import V5, Info, VersionInfo


class Latte(V5):
    def __init__(self):
        super(Latte, self).__init__()
        self._botInfo: Info = Info(name='Latte', version=VersionInfo(major=0, minor=1, micro=0, releaselevel='dev', serial=0))

    @property
    def info(self) -> Info:
        return self._botInfo