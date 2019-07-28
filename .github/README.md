# Hybrid Iterator Home
[heading__title]:
  #hybrid-iterator-home
  "&#x2B06; Top of ReadMe File"


Python 2/3 iterator cross-bred with a Dictionary


## [![Byte size of __init__.py][badge__master__hybrid_iterator__source_code]][hybrid_iterator__master__source_code] [![Open Issues][badge__issues__hybrid_iterator]][issues__hybrid_iterator] [![Open Pull Requests][badge__pull_requests__hybrid_iterator]][pull_requests__hybrid_iterator] [![Latest commits][badge__commits__hybrid_iterator__master]][commits__hybrid_iterator__master]



------


#### Table of Contents


- [:arrow_up: Top of ReadMe File][heading__title]

- [:zap: Quick Start][heading__quick_start]

  - [:memo: Edit Your ReadMe File][heading__your_readme_file]
  - [:snake: Utilize Hybrid Iterator][heading__utilize]
  - [:floppy_disk: Commit and Push][heading__commit_and_push]

- [&#x1F5D2; Notes][heading__notes]

- [&#x2696; License][heading__license]


------



## Quick Start
[heading__quick_start]:
  #quick-start
  "&#9889; Perhaps as easy as one, 2.0,..."


**Bash Variables**


```Bash
_module_name='hybrid-iterator'
_module_https_url="https://github.com/python-utilities/${_module_name}.git"
_module_relative_path="lib/modules/${_module_name}"
```


**Bash Submodule Commands**


```Bash
cd "<your-git-project-path>"

git checkout masters
mkdir -vp "lib/modules"

git submodule add\
 -b master --name "${_module_name}"\
 "${_module_https_url}" "${_module_relative_path}"
```


### Your ReadMe File
[heading__your_readme_file]:
  #your-readme-file
  "&#x1F4DD; Suggested additions for your ReadMe.md file so everyone has a good time with submodules"


Suggested additions for your _`ReadMe.md`_ file so everyone has a good time with submodules


```MarkDown
Clone with the following to avoid incomplete downloads


    git clone --recurse-submodules <url-for-your-project>


Update/upgrade submodules via


    git submodule update --init --merge --recursive
```


### Utilize Hybrid Iterator
[heading__utilize]:
  #utilize-hybrid-iterator
  "&#x1F40D; How to make use of this submodule within another project"


```Python
#!/usr/bin/env python


from lib.hybrid-iterator import Hybrid_Iterator


class Priority_Buffer(Hybrid_Iterator):
    """
    Priority_Buffer

    ## Arguments

    - `graph`, with `{name: sub_graph}` and `sub_graph[key_name]` to compare
    - `buffer_size`, `int` of desired `{name: sub_graph}` pairs to buffer
    - `priority`, dictionary containing the following data structure
        - `key_name`, withing `graph` to compare with `_bound`s bellow
        - `GE_bound`, buffers those greater than or equal to `graph[key_name]`
        - `LE_bound`, buffers those less than or equal to `graph[key_name]`
    - `step`, dictionary containing the following `{key: value}` pairs
        - `amount`, to increment or decrement `_bound`s to ensure full buffer
        - `GE_min`/`LE_max`, bounds the related `_bounds` above
    - `modifier` if set __must__ accept `{key: value}` pairs from `graph`
    """

    def __init__(self, graph, priority, buffer_size, step, modifier = None, **kwargs):
        super(Priority_Buffer, self).__init__(**kwargs)
        self.update(
            graph = graph,
            priority = priority,
            buffer_size = buffer_size,
            step = step,
            modifier = modifier,
            buffer = {})

    @property
    def is_buffered(self):
        """
        Returns `True` if buffer is satisfied or graph is empty, `False`
        otherwise. Used by `next()` to detect conditions to `return` on.
        """
        if len(self['buffer'].keys()) >= self['buffer_size']:
            return True

        if len(self['graph'].keys()) <= 0:
            return True

        if self['step'].get('GE_min') is not None:
            if self['priority']['GE_bound'] < self['step']['GE_min']:
                return True
        elif self['step'].get('LE_max') is not None:
            if self['priority']['LE_bound'] > self['step']['LE_max']:
                return True
        else:
            raise ValueError("self['priority'] missing step missing min/max")

        return False

    def top_priority(self, graph = None):
        """
        Yields `dict`s from `graph` where value of `graph[key_name]`,
        as set by `self['priority']['key_name']`, is within range of
        `self['GE_bound']` or `self['LE_bound']`

        - `graph`, dictionary that is __destructively__ read (`pop`ed) from

        > if `graph` is `None` then `top_priority` reads from `self['graph']`
        """
        if graph is None:
            graph = self['graph']

        key_name = self['priority']['key_name']
        for name, node in graph.items():
            if self['priority'].get('GE_bound') is not None:
                if node[key_name] >= self['priority']['GE_bound']:
                    yield {name: graph.pop(name)}
            elif self['priority'].get('LE_bound') is not None:
                if node[key_name] <= self['priority']['LE_bound']:
                    yield {name: graph.pop(name)}
            else:
                raise ValueError('Misconfiguration, either `GE_`/`LE_bound`s ')

        self.throw(GeneratorExit)

    def next(self):
        """
        Sets `self['buffer']` from `self.top_priority()` and returns `self`
        """
        if not self['graph']:
            self.throw(GeneratorExit)

        self['buffer'] = {}
        priority_gen = self.top_priority()
        while not self.is_buffered:
            try:
            except (StopIteration, GeneratorExit):
                if self['priority'].get('GE_bound'):
                    self['priority']['GE_bound'] += self['step']['amount']
                    priority_gen = self.top_priority()
                elif self['priority'].get('LE_bound'):
                    self['priority']['LE_bound'] += self['step']['amount']
                    priority_gen = self.top_priority()
                else:
                    raise ValueError("self['priority'] missing bounds")
            else:
                try:
                    self['buffer'].update(self['modifier'](next_sub_graph))
                except TypeError:
                    self['buffer'].update(next_sub_graph)

        return self


if __name__ == '__main__':
    """
    The following are run when this file is executed as
    a script, eg. `python priority_buffer.py`
    but not executed when imported as a module, thus a
    good place to put unit tests.
    """
    from random import randint

    print("Initalizing unit test.\n{0}".format("".join(['_' for x in range(9)])))
    graph = {}
    for i in range(0, 21, 1):
        graph.update({
            "sub_graph_{0}".format(i): {
                'points': {},
                'first_to_compute': randint(0, 9),
            }
        })

    print("Sample graph head.\n{0}".format("".join(['_' for x in range(9)])))
    head_counter = 0
    for k, v in graph.items():
        print("{0} -> {1}".format(k, v))
        head_counter += 1
        if head_counter > 3:
            break

    buffer = Priority_Buffer(
        graph = graph,
        priority = {'key_name': 'first_to_compute',
                    'GE_bound': 7},
        step = {'amount': -2,
                'GE_min': -1},
        buffer_size = 5,
    )

    print("Iterating over sample graph.\n{0}".format("".join(['_' for x in range(9)])))
    counter = 0
    c_max = int(len(graph.keys()) / buffer['buffer_size'] + 1)
    # ... (21 / 5) + 1 -> int -> 5
    for chunk in buffer:
        print("Chunk {count} of ~ {max}".format(
            count = counter, max = c_max - 1))

        for key, val in chunk['buffer'].items():
            print("\t{k} -> {v}".format(**{
                'k': key, 'v': val}))

        counter += 1

        if counter > c_max:
            raise Exception("Hunt for bugs!")

    print("Finished test.\n{0}".format("".join(['_' for x in range(9)])))
```


### Commit and Push
[heading__commit_and_push]:
  #commit-and-push
  "&#x1F4BE; It may be just this easy..."


```Bash
git add .gitmodules
git add lib/modules/hybrid-iterator


## Add any changed files too


git commit -F- <<'EOF'
:heavy_plus_sign: Adds `python-utilities/hybrid-iterator#1` submodule



**Additions**


- `.gitmodules`, tracks submodules AKA Git within Git _fanciness_

- `README.md`, updates installation and updating guidance

- `lib/modules/hybrid-iterator`, builds list of pages for a named collection
EOF


git push origin master
```


**:tada: Excellent :tada:** your repository is now ready to begin unitizing code from this project!


___


## Notes
[heading__notes]:
  #notes
  "&#x1F5D2; Additional resources and things to keep in mind when developing"


Hybrid Iterator is intended for importing and modification, and **not** for stand-alone use.

___


## License
[heading__license]:
  #license
  "&#x2696; Legal bits of Open Source software"


Legal bits of Open Source software


```
Hybrid Iterator ReadMe documenting how things like this could be utilized
Copyright (C) 2019  S0AndS0

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation; version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```



[badge__commits__hybrid_iterator__master]:
  https://img.shields.io/github/last-commit/python-utilities/hybrid-iterator/master.svg

[commits__hybrid_iterator__master]:
  https://github.com/python-utilities/hybrid-iterator/commits/master
  "&#x1F4DD; History of changes on this branch"


[hybrid_iterator__community]:
  https://github.com/python-utilities/hybrid-iterator/community
  "&#x1F331; Dedicated to functioning code"


[hybrid_iterator__gh_pages]:
  https://github.com/python-utilities/hybrid-iterator/tree/gh-pages
  "Source code examples hosted thanks to GitHub Pages!"



[badge__demo__hybrid_iterator]:
  https://img.shields.io/website/https/python-utilities.github.io/hybrid-iterator/index.html.svg?down_color=darkorange&down_message=Offline&label=Demo&logo=Demo%20Site&up_color=success&up_message=Online

[demo__hybrid_iterator]:
  https://python-utilities.github.io/hybrid-iterator/index.html
  "&#x1F52C; Check the example collection tests"


[badge__issues__hybrid_iterator]:
  https://img.shields.io/github/issues/python-utilities/hybrid-iterator.svg

[issues__hybrid_iterator]:
  https://github.com/python-utilities/hybrid-iterator/issues
  "&#x2622; Search for and _bump_ existing issues or open new issues for project maintainer to address."


[badge__pull_requests__hybrid_iterator]:
  https://img.shields.io/github/issues-pr/python-utilities/hybrid-iterator.svg

[pull_requests__hybrid_iterator]:
  https://github.com/python-utilities/hybrid-iterator/pulls
  "&#x1F3D7; Pull Request friendly, though please check the Community guidelines"


[badge__master__hybrid_iterator__source_code]:
  https://img.shields.io/github/size/python-utilities/hybrid-iterator/__init__.py.svg?label=__init__.py

[hybrid_iterator__master__source_code]:
  https://github.com/python-utilities/hybrid-iterator/blob/master/__init__.py
  "&#x2328; Project source, one Python file of importable code!"
