import jsonref


def dispatch(v):
    if 'anyOf' in v:
        return handle_union(v)

    t = v['type']

    if t == 'object':
        return handle_object(v)

    if t == 'array':
        return handle_array(v)

    if t == 'string':
        return 'string'

    if t == 'boolean':
        return 'boolean'

    if t == 'integer':
        return 'int'

    if t == 'number':
        return 'float'

    raise Exception(f'unknown type: {t}')


def handle_union(o):
    res = [dispatch(v) for v in o['anyOf']]
    res = ','.join(res)
    return f'union<{res}>'

def map_dispatch(o: dict):
    return [(k, dispatch(v)) for k, v in o['properties'].items()]


def handle_object(o: dict):
    res = [f'{k}:{v}' for (k,v) in map_dispatch(o)]
    res = ','.join(res)
    return f'struct<{res}>'


def handle_array(o: dict):
    t = dispatch(o['items'])
    return f'array<{t}>'


def handle_root(o: dict):
    return map_dispatch(o)


def convert(schema):
    if not schema:
        return []

    schema = jsonref.loads(schema)
    return handle_root(schema)
