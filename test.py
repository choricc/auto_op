#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/9 17:55
# @Author  : Lani
# @File    : guitest.py

from gooey import Gooey, GooeyParser


@Gooey(program_name="checkBoxTest")
def gui_main():
    parser = GooeyParser(description="checkBoxTest")
    parser.add_argument("-cb", "--test1", widget="CheckBox", action="store_true", help="test1")
    #
    parser.add_argument(
        '-f', '--foo',
        metavar='Some Flag',
        action='store_true',
        help='I turn things on and off')

    args = parser.parse_args()
    print(args)
    if args.test1:
        print("test 勾选了")
    else:
        print("test1 未勾选")

    if args.foo:
        print("foo 勾选了")
    else:
        print("foo 未勾选")


if __name__ == "__main__":
    gui_main()