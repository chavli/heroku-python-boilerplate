from enum import Enum, auto


class AutoNamedEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __str__(self):
        s = self.name.replace("_", " ").title()
        return s

    def __repr__(self):
        return self.name

    def describe(self):
        return self.name, self.value

    @classmethod
    def names(cls):
        return set([name for name, value in cls.__members__.items()])


    @classmethod
    def get(cls, name: str):
        try:
            value = cls[name]
        except KeyError:
            value = None
        finally:
            return value
