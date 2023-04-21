# argument classes to extract flags/kwargs from user input


import re

__all__ = (
    'ArgumentWithFlags',
)


class ArgumentWithFlags:
    def __init__(self, value: str):
        self.value = value

    @property
    def flags(self) -> list[str]:
        return re.findall(r'-\w', self.value)

    @property
    def kwargs(self):
        return {
            kwarg.split('=')[0]: kwarg.split('=')[1]
            for kwarg in re.findall(r'\w=\S*', self.value)
        }