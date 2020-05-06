from ....binary import BinaryReader, BinaryWriter
from ....binary.types import Int8, String, UInt32
from ....classes.util.signature_map import HKSignatureMap

if False:
    from .hkclassnamessection import HKClassnamesSection


class HKClass:
    signature: UInt32
    name: String
    offset: UInt32

    def read(self, csec: "HKClassnamesSection", br: BinaryReader):
        self.signature = br.read_uint32()
        br.assert_int8(Int8(0x09))  # Delimiter between class name and signature
        self.offset = br.tell() - csec.absolute_offset
        self.name = br.read_string()

    def write(self, csec: "HKClassnamesSection", bw: BinaryWriter):
        bw.write_uint32(self.signature)
        bw.write_int8(Int8(0x09))
        self.offset = bw.tell() - csec.absolute_offset
        bw.write_string(self.name)

    @classmethod
    def from_name(cls, name: String):
        inst = cls()
        inst.name = name
        inst.signature = HKSignatureMap.get(name)

        return inst

    def __repr__(self):
        return f"<{self.name}({self.offset})>"