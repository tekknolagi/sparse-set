from __future__ import annotations
import dataclasses
import unittest

# Port of https://gist.github.com/robalni/311afd0756f25c4f234b2ae332cd0bdc

def hash(s):
    # Stable hash function not depending on PYTHONHASHSEED
    prime = 0x100000001b3
    result = 0xcbf29ce484222325
    for c in s:
        result ^= ord(c)
        result *= prime
    return result

@dataclasses.dataclass
class Hamt:
    key: str = None
    value: object = None
    children: list[Hamt|None] = dataclasses.field(default_factory=lambda: [None, None])

    def find(self, key: str):
        h = hash(key)
        result = self
        while (result := result.children[h & 1]):
            if result.key == key: break
            h >>= 1
        return result

    def add(self, kv: Hamt):
        h = hash(kv.key)
        result = self
        prev = None
        while (prev := result) and (result := result.children[h & 1]):
            if result.key == kv.key: break
            h >>= 1
        if not prev.children[h & 1]:
            prev.children[h & 1] = kv

class HamtTests(unittest.TestCase):
    def test_create_root(self):
        root = Hamt()
        self.assertEqual(root.key, None)
        self.assertEqual(root.value, None)
        self.assertIsInstance(root.children, list)
        self.assertEqual(root.children, [None, None])
        other = Hamt()
        self.assertIsNot(root.children, other.children)

    def test_add(self):
        root = Hamt()
        a = Hamt("a", 1)
        root.add(a)
        self.assertEqual(root, Hamt(None, None, [a, None]))
        b = Hamt("b", 2)
        root.add(b)
        self.assertEqual(a, Hamt("a", 1, [None, None]))
        self.assertEqual(root, Hamt(None, None, [a, b]))
        c = Hamt("c", 3)
        root.add(c)
        self.assertEqual(root.find("a"), a)
        self.assertEqual(root.find("b"), b)
        self.assertEqual(root.find("c"), c)
        self.assertEqual(a, Hamt("a", 1, [None, c]))
        self.assertEqual(b, Hamt("b", 2, [None, None]))
        self.assertEqual(c, Hamt("c", 3, [None, None]))
        self.assertEqual(root, Hamt(None, None, [a, b]))
        d = Hamt("d", 4)
        root.add(d)
        self.assertEqual(root.find("d"), d)
        self.assertEqual(a, Hamt("a", 1, [None, c]))
        self.assertEqual(b, Hamt("b", 2, [None, d]))
        self.assertEqual(c, Hamt("c", 3, [None, None]))
        self.assertEqual(d, Hamt("d", 4, [None, None]))
        self.assertEqual(root, Hamt(None, None, [a, b]))

    def test_find(self):
        root = Hamt()
        self.assertIs(root.find("a"), None)
        a = Hamt("a", 1)
        self.assertIs(Hamt(None, None, [a, None]).find("a"), a)
        b = Hamt("b", 2)
        self.assertIs(Hamt(None, None, [a, b]).find("b"), b)

if __name__ == "__main__":
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999
    unittest.main()
