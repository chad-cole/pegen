#!/usr/bin/env python3.8
# @generated by pegen.py from pegen/metagrammar.gram
from __future__ import annotations

import ast
import sys
import tokenize

from pegen.grammar import (
    Alt,
    Group,
    NameLeaf,
    NamedItem,
    NegativeLookahead,
    Opt,
    PositiveLookahead,
    Repeat0,
    Repeat1,
    Rhs,
    Rule,
    Grammar,
    StringLeaf,
)
from pegen.parser import memoize, memoize_left_rec, logger, Parser


class GeneratedParser(Parser):

    @memoize
    def start(self):
        # start: rules $ { Grammar ( rules ) }
        mark = self.mark()
        cut = False
        if (
            (rules := self.rules())
            and
            (endmarker := self.expect('ENDMARKER'))
        ):
            return Grammar ( rules )
        self.reset(mark)
        if cut: return None
        return None

    @memoize
    def rules(self):
        # rules: rule rules { [ rule ] + rules } | rule { [ rule ] }
        mark = self.mark()
        cut = False
        if (
            (rule := self.rule())
            and
            (rules := self.rules())
        ):
            return [ rule ] + rules
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (rule := self.rule())
        ):
            return [ rule ]
        self.reset(mark)
        if cut: return None
        return None

    @memoize
    def rule(self):
        # rule: rulename ":" alts NEWLINE INDENT more_alts DEDENT { Rule ( * rulename , alts . alts + more_alts . alts ) } | rulename ":" NEWLINE INDENT more_alts DEDENT { Rule ( * rulename , more_alts ) } | rulename ":" alts NEWLINE { Rule ( * rulename , alts ) }
        mark = self.mark()
        cut = False
        if (
            (rulename := self.rulename())
            and
            (literal := self.expect(":"))
            and
            (alts := self.alts())
            and
            (newline := self.expect('NEWLINE'))
            and
            (indent := self.expect('INDENT'))
            and
            (more_alts := self.more_alts())
            and
            (dedent := self.expect('DEDENT'))
        ):
            return Rule ( * rulename , alts . alts + more_alts . alts )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (rulename := self.rulename())
            and
            (literal := self.expect(":"))
            and
            (newline := self.expect('NEWLINE'))
            and
            (indent := self.expect('INDENT'))
            and
            (more_alts := self.more_alts())
            and
            (dedent := self.expect('DEDENT'))
        ):
            return Rule ( * rulename , more_alts )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (rulename := self.rulename())
            and
            (literal := self.expect(":"))
            and
            (alts := self.alts())
            and
            (newline := self.expect('NEWLINE'))
        ):
            return Rule ( * rulename , alts )
        self.reset(mark)
        if cut: return None
        return None

    @memoize
    def rulename(self):
        # rulename: NAME '[' type=NAME '*' ']' { ( name . string , type . string + "*" ) } | NAME '[' type=NAME ']' { ( name . string , type . string ) } | NAME { ( name . string , None ) }
        mark = self.mark()
        cut = False
        if (
            (name := self.name())
            and
            (literal := self.expect('['))
            and
            (type := self.name())
            and
            (literal_1 := self.expect('*'))
            and
            (literal_2 := self.expect(']'))
        ):
            return ( name . string , type . string + "*" )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (name := self.name())
            and
            (literal := self.expect('['))
            and
            (type := self.name())
            and
            (literal_1 := self.expect(']'))
        ):
            return ( name . string , type . string )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (name := self.name())
        ):
            return ( name . string , None )
        self.reset(mark)
        if cut: return None
        return None

    @memoize
    def alts(self):
        # alts: alt "|" alts { Rhs ( [ alt ] + alts . alts ) } | alt { Rhs ( [ alt ] ) }
        mark = self.mark()
        cut = False
        if (
            (alt := self.alt())
            and
            (literal := self.expect("|"))
            and
            (alts := self.alts())
        ):
            return Rhs ( [ alt ] + alts . alts )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (alt := self.alt())
        ):
            return Rhs ( [ alt ] )
        self.reset(mark)
        if cut: return None
        return None

    @memoize
    def more_alts(self):
        # more_alts: "|" alts NEWLINE more_alts { Rhs ( alts . alts + more_alts . alts ) } | "|" alts NEWLINE { Rhs ( alts . alts ) }
        mark = self.mark()
        cut = False
        if (
            (literal := self.expect("|"))
            and
            (alts := self.alts())
            and
            (newline := self.expect('NEWLINE'))
            and
            (more_alts := self.more_alts())
        ):
            return Rhs ( alts . alts + more_alts . alts )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (literal := self.expect("|"))
            and
            (alts := self.alts())
            and
            (newline := self.expect('NEWLINE'))
        ):
            return Rhs ( alts . alts )
        self.reset(mark)
        if cut: return None
        return None

    @memoize
    def alt(self):
        # alt: items '$' action { Alt ( items + [ NamedItem ( None , NameLeaf ( 'ENDMARKER' ) ) ] , action = action ) } | items '$' { Alt ( items + [ NamedItem ( None , NameLeaf ( 'ENDMARKER' ) ) ] , action = None ) } | items action { Alt ( items , action = action ) } | items { Alt ( items , action = None ) }
        mark = self.mark()
        cut = False
        if (
            (items := self.items())
            and
            (literal := self.expect('$'))
            and
            (action := self.action())
        ):
            return Alt ( items + [ NamedItem ( None , NameLeaf ( 'ENDMARKER' ) ) ] , action = action )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (items := self.items())
            and
            (literal := self.expect('$'))
        ):
            return Alt ( items + [ NamedItem ( None , NameLeaf ( 'ENDMARKER' ) ) ] , action = None )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (items := self.items())
            and
            (action := self.action())
        ):
            return Alt ( items , action = action )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (items := self.items())
        ):
            return Alt ( items , action = None )
        self.reset(mark)
        if cut: return None
        return None

    @memoize
    def items(self):
        # items: named_item items { [ named_item ] + items } | named_item { [ named_item ] }
        mark = self.mark()
        cut = False
        if (
            (named_item := self.named_item())
            and
            (items := self.items())
        ):
            return [ named_item ] + items
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (named_item := self.named_item())
        ):
            return [ named_item ]
        self.reset(mark)
        if cut: return None
        return None

    @memoize
    def named_item(self):
        # named_item: NAME '=' item { NamedItem ( name . string , item ) } | item { NamedItem ( None , item ) } | item=lookahead { NamedItem ( None , item ) }
        mark = self.mark()
        cut = False
        if (
            (name := self.name())
            and
            (literal := self.expect('='))
            and
            (item := self.item())
        ):
            return NamedItem ( name . string , item )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (item := self.item())
        ):
            return NamedItem ( None , item )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (item := self.lookahead())
        ):
            return NamedItem ( None , item )
        self.reset(mark)
        if cut: return None
        return None

    @memoize
    def lookahead(self):
        # lookahead: '&' atom { PositiveLookahead ( atom ) } | '!' atom { NegativeLookahead ( atom ) } | '~' { NameLeaf ( 'CUT' ) }
        mark = self.mark()
        cut = False
        if (
            (literal := self.expect('&'))
            and
            (atom := self.atom())
        ):
            return PositiveLookahead ( atom )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (literal := self.expect('!'))
            and
            (atom := self.atom())
        ):
            return NegativeLookahead ( atom )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (literal := self.expect('~'))
        ):
            return NameLeaf ( 'CUT' )
        self.reset(mark)
        if cut: return None
        return None

    @memoize
    def item(self):
        # item: '[' alts ']' { Opt ( alts ) } | atom '?' { Opt ( atom ) } | atom '*' { Repeat0 ( atom ) } | atom '+' { Repeat1 ( atom ) } | atom { atom }
        mark = self.mark()
        cut = False
        if (
            (literal := self.expect('['))
            and
            (alts := self.alts())
            and
            (literal_1 := self.expect(']'))
        ):
            return Opt ( alts )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (atom := self.atom())
            and
            (literal := self.expect('?'))
        ):
            return Opt ( atom )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (atom := self.atom())
            and
            (literal := self.expect('*'))
        ):
            return Repeat0 ( atom )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (atom := self.atom())
            and
            (literal := self.expect('+'))
        ):
            return Repeat1 ( atom )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (atom := self.atom())
        ):
            return atom
        self.reset(mark)
        if cut: return None
        return None

    @memoize
    def atom(self):
        # atom: '(' alts ')' { Group ( alts ) } | NAME { NameLeaf ( name . string ) } | STRING { StringLeaf ( string . string ) }
        mark = self.mark()
        cut = False
        if (
            (literal := self.expect('('))
            and
            (alts := self.alts())
            and
            (literal_1 := self.expect(')'))
        ):
            return Group ( alts )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (name := self.name())
        ):
            return NameLeaf ( name . string )
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (string := self.string())
        ):
            return StringLeaf ( string . string )
        self.reset(mark)
        if cut: return None
        return None

    @memoize
    def action(self):
        # action: "{" target_atoms "}" { target_atoms }
        mark = self.mark()
        cut = False
        if (
            (literal := self.expect("{"))
            and
            (target_atoms := self.target_atoms())
            and
            (literal_1 := self.expect("}"))
        ):
            return target_atoms
        self.reset(mark)
        if cut: return None
        return None

    @memoize
    def target_atoms(self):
        # target_atoms: target_atom target_atoms { target_atom + " " + target_atoms } | target_atom { target_atom }
        mark = self.mark()
        cut = False
        if (
            (target_atom := self.target_atom())
            and
            (target_atoms := self.target_atoms())
        ):
            return target_atom + " " + target_atoms
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (target_atom := self.target_atom())
        ):
            return target_atom
        self.reset(mark)
        if cut: return None
        return None

    @memoize
    def target_atom(self):
        # target_atom: "{" target_atoms "}" { "{" + target_atoms + "}" } | NAME { name . string } | NUMBER { number . string } | STRING { string . string } | !"}" OP { op . string }
        mark = self.mark()
        cut = False
        if (
            (literal := self.expect("{"))
            and
            (target_atoms := self.target_atoms())
            and
            (literal_1 := self.expect("}"))
        ):
            return "{" + target_atoms + "}"
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (name := self.name())
        ):
            return name . string
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (number := self.number())
        ):
            return number . string
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            (string := self.string())
        ):
            return string . string
        self.reset(mark)
        if cut: return None
        cut = False
        if (
            self.negative_lookahead(self.expect, "}")
            and
            (op := self.op())
        ):
            return op . string
        self.reset(mark)
        if cut: return None
        return None


if __name__ == '__main__':
    from pegen.parser import simple_parser_main
    simple_parser_main(GeneratedParser)
