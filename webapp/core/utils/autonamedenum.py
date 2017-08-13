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

    @property
    def description(self) -> str:
        """ return the ENUM value description """
        return self.desc

    @description.setter
    def description(self, desc: str):
        """ add a description for an ENUM value. not related to describe() """
        self.desc = desc

    @classmethod
    def names(cls):
        return set(name for name, value in cls.__members__.items())

    @classmethod
    def get(cls, name: str):
        try:
            value = cls[name]
        except KeyError:
            value = None
        finally:
            return value
