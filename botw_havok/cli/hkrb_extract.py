import argparse
import json
import os
from copy import deepcopy
from typing import List

from .. import Havok
from ..binary.types import UInt32
from ..classes.common.ActorInfo import ActorInfo
from .common import Fore, Messages, init, shapes_to_hkrb


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract HKRB actor collision from a single HKSC compound file"
    )
    parser.add_argument("hkscFile", help="Path to a Havok StaticCompound file")
    parser.add_argument("hashId", type=UInt32, help="HashId to extract")
    parser.add_argument(
        "outFile", help="Path to the destination Havok RigidBody file", nargs="?"
    )

    return parser.parse_args()


def binary_search(l: List[ActorInfo], hashId: UInt32):
    first = 0
    last = len(l) - 1

    while first <= last:
        mid = (first + last) // 2
        if l[mid].HashId == hashId:
            return l[mid]
        else:
            if hashId > l[mid].HashId:
                first = mid + 1
            else:
                last = mid - 1

    raise SystemExit(f"HashId '{hashId}' doesn't exist in this StaticCompound file!")


def main():
    init(autoreset=True)

    args = parse_args()

    Messages.loading(args.hkscFile)
    hk = Havok.from_file(args.hkscFile)

    Messages.deserializing(args.hkscFile)
    hk.deserialize()

    Messages.check_type(hk, "hksc")

    nx = hk.files[0].header.pointer_size == 8

    import time

    start = time.time()
    print(f"{Fore.BLUE}Seaching for HashId '{args.hashId}'")
    ai = binary_search(hk.files[0].data.contents[0].ActorInfo, args.hashId)
    print(f"found it in: {time.time()-start}")

    shapes = [
        instance.shape
        for rigidbody in hk.files[1]
        .data.contents[0]
        .namedVariants[0]
        .variant.systems[0]
        .rigidBodies
        for instance in rigidbody.collidable.shape.instances
        if instance.userData in range(ai.ShapeInfoStart, ai.ShapeInfoEnd + 1)
    ]

    shapes_to_hkrb(shapes, args.hkscFile, args.outFile, nx)


if __name__ == "__main__":
    main()
