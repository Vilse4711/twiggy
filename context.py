from types import ListType, TupleType
from module import *


def encode(modules):
    new = []
    for m in modules:
        if type(m) == ListType or type(m) == TupleType:
            new.append(LB)
            new.extend(encode(m))
            new.append(RB)
        else:
            new.append(m)
    return new


def skipLeft(modules, index):
    """skipLeft(): Skip up to the next unbalanced LB() (left bracket)"""
    # Assume we are on a branch
    count = 1
    i = index
    while count > 0 and i > 0:
        module = modules[i]
        if isinstance(module, LB):
            count = count - 1
        elif isinstance(module, RB):
            count = count + 1
        i = i - 1
    return i


def skipRight(modules, index):
    """skipRight(): Skip up to the next unbalanced RB() (right bracket)"""
    # Assume we are on a branch
    count = 1
    i = index
    while count > 0 and i < len(modules):
        module = modules[i]
        if isinstance(module, RB):
            count = count - 1
        elif isinstance(module, LB):
            count = count + 1
        i = i + 1
    return i - 1


def matchStrictForward(md, actuals, mpos):
    for formal in md.formals:
        candidate = md.modules[mpos]
        if isinstance(candidate, formal):
            actuals.append(candidate)
        else:
            return False, None

        mpos = mpos + 1

        if mpos > len(md.modules):
            return False, None
    return True, actuals


def matchLeftwards(md, actuals, fpos, mpos):
    if fpos < 0:
        # We have matched all of the left context
        actuals.reverse()  # Everything is in the reversed order
        return True, actuals
    elif fpos >= 0 and mpos < 0:
        # Failed to match because we ran out of modules
        return False, None

    formal = md.formals[fpos]
    candidate = md.modules[mpos]

    if isinstance(candidate, formal):
        # Have a partial match, save it and try to match rest
        if not isinstance(candidate, (LB, RB)):
            # Not interested in saving brackets
            actuals.append(candidate)
        return matchLeftwards(md, actuals, fpos - 1, mpos - 1)
    elif isinstance(candidate, md.consider):
        # Fail to match
        return False, None
    elif isinstance(candidate, md.ignore):
        # Ignore this candidate
        return matchLeftwards(md, actuals, fpos, mpos - 1)
    elif not issubclass(formal, LB) and isinstance(candidate, LB):
        # Figure 9
        return matchLeftwards(md, actuals, fpos, mpos - 1)
    elif not issubclass(formal, RB) and isinstance(candidate, RB):
        # Figure 10
        return matchLeftwards(md, actuals, fpos, skipLeft(md.modules, mpos - 1))
    else:
        # Fail to match
        return False, None


def matchRightwards(md, actuals, fpos, mpos):
    if fpos >= len(md.formals):
        # We have matched all of the right context
        return True, actuals
    elif fpos < len(md.formals) and mpos >= len(md.modules):
        # Failed to match because we ran out of modules
        return False, None

    formal = md.formals[fpos]
    candidate = md.modules[mpos]

    if isinstance(candidate, formal):
        # We have a partial match, match rest
        if not isinstance(candidate, (LB, RB)):
            # Not interested in saving brackets
            actuals.append(candidate)
        return matchRightwards(md, actuals, fpos + 1, mpos + 1)
    elif isinstance(candidate, md.consider):
        # Fail to match
        return False, None
    elif isinstance(candidate, md.ignore):
        # Move on and ignore this actual
        return matchRightwards(md, actuals, fpos, mpos + 1)
    elif not issubclass(formal, LB) and isinstance(candidate, LB):
        # Figure 5
        return matchRightwards(md, actuals, fpos, skipRight(md.modules, mpos + 1) + 1)  # Skip past the last RB
    elif issubclass(formal, RB):  # We know that candidate is not an RB
        # Figure 6 & 8
        return matchRightwards(md, actuals, fpos,
                               skipRight(md.modules, mpos + 1))  # Skip upto a possible RB or another module
    else:
        # Failed to match
        return False, None


class MatchData:
    """Contains constant parameters used during matching"""

    def __init__(self, modules, formals, consider, ignore):
        self.modules = modules
        self.formals = formals
        self.consider = consider
        self.ignore = ignore


class FSC:
    """FSC() - Formal Standard Context
       lc - left context
       sp - strict predecessor
       rc - right context
    """

    def __init__(self, lc, sp, rc):
        self.lc = lc
        self.sp = sp
        self.rc = rc
        self._encoded = False

    def __repr__(self):
        return "FSC(%s,%s,%s)" % (self.lc, self.sp, self.rc)

    def match(self, modules, mi, consider, ignore, **kwargs):
        """match() returns None or an Actual Context (AC).
           Direction is FC.FORWARD or FC.BACKWARD"""

        if 'direction' in kwargs.keys():
            direction = kwargs['direction']
        else:
            direction = FORWARD

        # Match strict predecessor
        md = MatchData(modules, self.sp, consider, ignore)
        if direction == FORWARD:
            success, strict = matchStrictForward(md, [], mi)
        elif direction == BACKWARD:
            # Not implemented
            assert False
        else:
            raise LException("Illegal value for direction. Has to be either FC.FORWARD or FC.BACKWARD!")

        if not success:
            return None

        # Match left context
        left = None
        if self.lc != None:
            md = MatchData(modules, self.lc, consider, ignore)
            if direction == FORWARD:
                success, left = matchLeftwards(md, [], 0, mi - 1)
            elif direction == BACKWARD:
                success, left = matchLeftwards(md, [], len(self.lc) - 1, mi - len(self.sp))

        if not success:
            return None

        # Match right context
        right = None
        if self.rc != None:
            md = MatchData(modules, self.rc, consider, ignore)
            if direction == FORWARD:
                success, right = matchRightwards(md, [], 0, mi + len(self.sp))
            elif direction == BACKWARD:
                success, right = matchRightwards(md, [], 0, mi + 1)

        if success:
            return ASC(left, strict, right)
        else:
            return None

    def numStrict(self):
        if self.sp != None:
            return len(strict)
        else:
            return 1

    def encoded(self):
        return self._encoded

    def encode(self):
        if self.rc != None:
            self.rc = encode(self.rc)
        if self.sp != None:
            self.sp = encode(self.sp)
        if self.lc != None:
            self.lc = encode(self.lc)
        self._encoded = True
        return self


class FNLC(FSC):
    """FNLC() - Formal New Left Context"""

    def __init__(self, nlc, lc, sp, rc):
        NFC.__init__(self, lc, sp, rc)
        self.nlc = nlc

    def match(self, modules, mi, direction):
        super(self, NFC).match(modules, mi, direction)


class FNRC(FSC):
    """FNRC() - Formal New Right Context"""

    def __init__(self, lc, sp, rc, nrc):
        NFC.__init__(self, lc, sp, rc)
        self.nrc = nrc

    def match(self, modules, mi, direction):
        super(self, NFC).match(modules, mi, direction)


FORWARD = 1
BACKWARD = -1


class ASC:
    """Actual Standard Context"""

    def __init__(self, lc, sp, rc):
        self.lc = lc
        self.sp = sp
        self.rc = rc

    def unpack(self, partId):
        if partId == ASC.LC:
            if self.lc != None and len(self.lc) == 1:
                return self.lc[0]
            else:
                return self.lc

        if partId == ASC.SP:
            if self.sp != None and len(self.sp) == 1:
                return self.sp[0]
            else:
                return self.sp

        if partId == ASC.RC:
            if self.rc != None and len(self.rc) == 1:
                return self.rc[0]
            else:
                return self.rc

        raise LException("Unknown partId:" + str(partId))


ASC.LC = 1
ASC.SP = 2
ASC.RC = 3

if __name__ == "__main__":
    class A(Module):
        def __repr__(self):
            return "A()"


    class B(Module):
        def __repr__(self):
            return "B()"


    class C(Module):
        def __repr__(self):
            return "C()"


    class D(Module):
        def __repr__(self):
            return "D()"


    # Figure 5 (A > C): Matching right context, lateral branches are implicitly ignored
    # String: A [ B ] C
    #         ^
    #    |
    # \  C
    #  B |
    #   \| The [ B ] branch is skipped
    #    |
    #    A
    #    |
    #
    _C = C()
    _A = A()
    modules = [_A, LB(), B(), RB(), _C]
    context = FSC(None, [A], [C]).flatten()
    actuals = context.match(modules, 0)
    _a = actuals.unpack(ASC.SP)
    _c = actuals.unpack(ASC.RC)
    assert _a == _A and _c == _C

    # Figure 6 (A > [ B ] C): Matching right context, remainder of lateral branch is implicitly ignored
    # String: A [ B D ] C
    #         ^
    # D   |
    #  \  C
    #   B |
    #    \| The D part of the [ B D ] branch is ignored
    #     |
    #     A
    #     |
    #
    _C = C()
    _A = A()
    _B = B()
    modules = [_A, LB(), _B, D(), RB(), _C]
    context = FSC(None, [A], [LB, B, RB, C]).flatten()
    actuals = context.match(modules, 0)
    _a = actuals.unpack(ASC.SP)
    _b, _c = actuals.unpack(ASC.RC)
    assert _a == _A and _b == _B and _c == _C

    # Figure 7 (A > [ B ] D): Problem with multiple lateral branches when matching the right context
    # String: A [ C ] [ B ] D
    #         ^
    #    |
    # \  D  /
    #  C | B
    #   \|/  Fails to match context [ C ] != [ b ]
    #    |
    #    A
    #    |
    #
    _A = A()
    _B = B()
    _D = D()
    modules = [_A, LB(), C(), RB(), LB(), _B, RB(), _D]
    context = FSC(None, [A], [LB, B, RB, D]).flatten()
    actuals = context.match(modules, 0)
    assert actuals == None

    # Figure 8 (A > [ ] [ B ] D): Explicit enumeration of lateral branches in the right context
    # String: A [ C ] [ B ] D
    #         ^
    #    |
    # \  D  /
    #  C | B
    #   \|/  The [ C ] branch is ignored
    #    |
    #    A
    #    |
    #
    _A = A()
    _B = B()
    _D = D()
    modules = [_A, LB(), C(), RB(), LB(), _B, RB(), _D]
    context = FSC(None, [A], [[], [B], D]).flatten()
    actuals = context.match(modules, 0)
    _a = actuals.unpack(ASC.SP)
    _b, _d = actuals.unpack(ASC.RC)
    assert _a == _A and _b == _B and _d == _D

    # Figure 9 (C < A): Matching left context, beginning of the branch implicitly ignored
    # String: C [ A ] B
    #             ^
    #    |
    # \  B
    #  A |
    #   \| The [ module is ignored
    #    |
    #    C
    #    |
    #
    _A = A()
    _C = C()
    modules = [_C, LB(), _A, RB(), B()]
    context = FSC([C], [A], None).flatten()
    actuals = context.match(modules, 2)
    _a = actuals.unpack(ASC.SP)
    _c = actuals.unpack(ASC.LC)
    assert _a == _A and _c == _C

    # Figure 10 (C < B): Matching left context, lateral branches implicitly ignored
    # String: C [ A ] B
    #                 ^
    #    |
    # \  B
    #  A |
    #   \| The [ A ] branch is ignored
    #    |
    #    C
    #    |
    #
    _B = B()
    _C = C()
    modules = [_C, LB(), A(), RB(), _B]
    context = FSC([C], [B], None).flatten()
    actuals = context.match(modules, 4)
    _b = actuals.unpack(ASC.SP)
    _c = actuals.unpack(ASC.LC)
    assert _b == _B and _c == _C
