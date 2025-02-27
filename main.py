import dataclasses
import unittest

# https://research.swtch.com/sparse

@dataclasses.dataclass
class SparseSet:
    sparse: list[int] = dataclasses.field(default_factory=list)
    dense: list[int] = dataclasses.field(default_factory=list)
    n: int = 0

    def add(self, i: int) -> None:
        if i in self:
            return
        self.dense.append(i)
        if i >= len(self.sparse):
            self.sparse.extend([None]*(i - len(self.sparse) + 1))
        self.sparse[i] = self.n
        self.n += 1

    def __contains__(self, i: int) -> bool:
        return i < len(self.sparse) and self.sparse[i] < self.n and self.dense[self.sparse[i]] == i

    def clear(self) -> None:
        self.n = 0

    def remove(self, i: int) -> None:
        if i not in self:
            return
        j = self.dense[self.n - 1]
        self.dense[self.sparse[i]] = j
        self.sparse[j] = self.sparse[i]
        self.n -= 1

    def __iter__(self):
        return iter(self.dense)

class SetTests(unittest.TestCase):
    def test_init(self):
        result = SparseSet()
        self.assertEqual(result.sparse, [])
        self.assertEqual(result.dense, [])
        self.assertEqual(result.n, 0)

    def test_add(self):
        result = SparseSet()
        result.add(3)
        result.add(4)
        self.assertEqual(result.sparse, [None, None, None, 0, 1])
        self.assertEqual(result.dense, [3, 4])
        result.add(3)
        self.assertEqual(result.sparse, [None, None, None, 0, 1])
        self.assertEqual(result.dense, [3, 4])

    def test_contains(self):
        result = SparseSet()
        self.assertNotIn(3, result)
        result.add(3)
        self.assertIn(3, result)
        self.assertNotIn(4, result)
        result.add(4)
        self.assertIn(4, result)

    def test_clear(self):
        result = SparseSet()
        result.add(3)
        self.assertIn(3, result)
        result.clear()
        self.assertNotIn(3, result)

    def test_remove(self):
        result = SparseSet()
        result.add(3)
        self.assertIn(3, result)
        result.remove(3)
        self.assertNotIn(3, result)

    def test_iter(self):
        result = SparseSet()
        self.assertEqual(list(iter(result)), [])
        result.add(3)
        result.add(4)
        self.assertEqual(list(iter(result)), [3, 4])

@dataclasses.dataclass
class SparseMap:
    sparse: list[int] = dataclasses.field(default_factory=list)
    dense: list[tuple[int, object]] = dataclasses.field(default_factory=list)
    n: int = 0

    def __setitem__(self, i: int, value: object) -> None:
        if i in self:
            self.dense[self.sparse[i]] = (i, value)
            return
        self.dense.append((i, value))
        if i >= len(self.sparse):
            self.sparse.extend([None]*(i - len(self.sparse) + 1))
        self.sparse[i] = self.n
        self.n += 1

    def __getitem__(self, i: int) -> None:
        if i >= len(self.sparse) or self.sparse[i] >= self.n:
            raise KeyError(i)
        result = self.dense[self.sparse[i]]
        if result[0] != i:
            raise KeyError(i)
        return result[1]

    def __contains__(self, i: int) -> bool:
        return i < len(self.sparse) and self.sparse[i] < self.n and self.dense[self.sparse[i]][0] == i

    def clear(self) -> None:
        self.n = 0

    def __delitem__(self, i: int) -> None:
        if i not in self:
            return
        j = self.dense[self.n - 1]
        self.dense[self.sparse[i]] = j
        self.sparse[j[0]] = self.sparse[i]
        self.n -= 1

    def __iter__(self):
        return iter(self.dense)

class MapTests(unittest.TestCase):
    def test_init(self):
        result = SparseMap()
        self.assertEqual(result.sparse, [])
        self.assertEqual(result.dense, [])
        self.assertEqual(result.n, 0)

    def test_setitem(self):
        result = SparseMap()
        result[3] = "a"
        result[4] = "b"
        self.assertEqual(result.sparse, [None, None, None, 0, 1])
        self.assertEqual(result.dense, [(3, "a"), (4, "b")])
        result[3] = "c"
        self.assertEqual(result.sparse, [None, None, None, 0, 1])
        self.assertEqual(result.dense, [(3, "c"), (4, "b")])

    def test_getitem(self):
        result = SparseMap()
        result[3] = "a"
        result[4] = "b"
        self.assertEqual(result[3], "a")
        self.assertEqual(result[4], "b")

    def test_contains(self):
        result = SparseMap()
        self.assertNotIn(3, result)
        result[3] = "a"
        self.assertIn(3, result)
        self.assertNotIn(4, result)
        result[4] = "b"
        self.assertIn(4, result)

    def test_clear(self):
        result = SparseMap()
        result[3] = "a"
        self.assertIn(3, result)
        result.clear()
        self.assertNotIn(3, result)

    def test_delitem(self):
        result = SparseMap()
        result[3] = "a"
        self.assertIn(3, result)
        del result[3]
        self.assertNotIn(3, result)

    def test_iter(self):
        result = SparseMap()
        self.assertEqual(list(iter(result)), [])
        result[3] = "a"
        result[4] = "b"
        self.assertEqual(list(iter(result)), [(3, "a"), (4, "b")])

if __name__ == "__main__":
    unittest.main()
