from j2g import convert
import sys
import json
import os

def cli():
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <module file> <class name>', file=sys.stderr)
        sys.exit(1)

    module_file = sys.argv[1].replace('.py', '')
    class_name = sys.argv[2]

    sys.path.append(os.path.dirname(module_file))

    imported = __import__(os.path.basename(module_file))
    imported = getattr(imported, class_name)
    schema = imported.schema_json()
    schema = convert(schema)
    schema = {k: v for (k,v) in schema}
    print(json.dumps(schema, indent=2))
