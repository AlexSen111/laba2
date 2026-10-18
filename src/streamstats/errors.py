class StreamStatsError(Exception):
    pass


class WrongTimeError(StreamStatsError):
    pass


class WrongLevelError(StreamStatsError):
    pass


class EmptySourceError(StreamStatsError):
    pass


class WrongEventError(StreamStatsError):
    pass
