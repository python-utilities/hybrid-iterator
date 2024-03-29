#!/usr/bin/env python


from collections import Iterator


license = """
Python class for combining Dictionary and Iterator classes.
Copyright (C) 2019 S0AndS0

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


class Hybrid_Iterator(dict, Iterator):
    """
    Contains _boilerplate_ and Python 2/3 compatibility for
    making a looping dictionary. Not intended to be used
    directly but instead to reduce redundant repetition.
    """

    def __init__(self, **kwargs):
        super(Hybrid_Iterator, self).__init__(**kwargs)

    def __iter__(self):
        return self

    def throw(self, type = None, traceback = None):
        raise StopIteration

    def next(self):
        """
        Inheriting classes **must** override this method to activate.

        - Called implicitly via `for` loops but maybe called explicitly.
        - `GeneratorExit`/`StopIteration` are an exit signal for loops.
        """
        self.throw(GeneratorExit)

    __next__ = next


if __name__ == '__main__':
    raise Exception("Hybrid_Iterator import and modify it to iterate dictionaries!")
