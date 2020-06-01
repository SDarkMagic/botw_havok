import json
import argparse

openFile = argparse.ArgumentParser(description="Converts a NavMesh JSON to an OBJ file.")
openFile.add_argument("fileToOpen", metavar="F", type=str, nargs=1,  help="The JSON file to be converted to a viewable OBJ format")
fileOpen = openFile.parse_args()
fileToOpen = fileOpen.fileToOpen[0]
print(fileToOpen)

def main():
    with open(fileToOpen, "r") as f:
        d = json.load(f)

    vertices = d[0]["data"]["contents"][0]["namedVariants"][0]["variant"]["vertices"]
    edges = [
        (edge["a"] + 1, edge["b"] + 1)
        for edge in d[0]["data"]["contents"][0]["namedVariants"][0]["variant"]["edges"]
    ]
    faces = d[0]["data"]["contents"][0]["namedVariants"][0]["variant"]["faces"]

    data = []
    for vtx in vertices:
        data.append(f'v {" ".join([str(f) for f in vtx])}')

    for face in faces:
        idxs = list(
            dict.fromkeys(
                [
                    x
                    for y in edges[
                        face["startEdgeIndex"] : face["startEdgeIndex"]
                        + face["numEdges"]
                    ]
                    for x in y
                ]
            )
        )
        data.append(f'f {" ".join([str(i) for i in idxs])}')

    with open(fileToOpen + ".obj", "w") as f:
        f.write("\n".join(data))


if __name__ == "__main__":
    main()