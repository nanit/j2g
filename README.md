# JSON Schema to AWS Glue schema converter

## Installation

```bash
pip install git+https://github.com/nanit/j2g.git
```

## What?

Converts `pydantic` schemas to `json schema` and then to `AWS glue schema`, so in theory anything that can be converted to JSON Schema *could* also work.

## Why?

When using `AWS Kinesis Firehose` in a configuration that receives JSONs and writes `parquet` files on S3, one needs to define a `AWS Glue` table so Firehose knows what schema to use when creating the parquet files.

AWS Glue let's you define a schema using `Avro` or `JSON Schema` and then to create a table from that schema, but as of *May 2022` there's a limitations on AWS that tables that are created that way can't be used with Kinesis Firehose.

https://stackoverflow.com/questions/68125501/invalid-schema-error-in-aws-glue-created-via-terraform

This is also confirmed by AWS support.

What one could do is create a table set the columns manually, but this means you now have two sources of truth to maintain.

This tool allows you to define a table in `pydantic` and generate a JSON with column types that can be used with `terraform` to create a Glue table.

## Example

Take the following pydantic class

```python
from pydantic import BaseModel
from typing import List

class Bar(BaseModel):
    name: str
    age: int

class Foo(BaseModel):
    nums: List[int]
    bars: List[Bar]
    other: str
```

Running `j2g`
```bash
python j2g example.py Foo
```

you get this JSON

```json
{
 "nums": "array<int>",
 "bars": "array<struct<name:string,age:int>>",
 "other": "string"
}
```

and can be used in terraform like that


```terraform
locals {
  columns = jsondecode(file("${path.module}/glue_schema.json"))
}

resource "aws_glue_catalog_table" "table" {
  name          = "table_name"
  database_name = "db_name"

  storage_descriptor {
    dynamic "columns" {
      for_each = local.columns

      content {
        name = columns.key
        type = columns.value
      }
    }
  }
}
```

## How it works?

* `pydantic` gets converted to JSON Schema
* the JSON Schema types get mapped to Glue types recursively

## Future work

* Not all types are supported, I just add types as I need them, but adding types is very easy, feel free to open issues or send a PR if you stumbled upon an non-supported use case
* the tool could be easily extended to working with JSON Schema directly
* thus anything that can be converted to a JSON Schema should also work.