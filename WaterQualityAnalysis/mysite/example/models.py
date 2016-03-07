import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.management import sync_table

class ExampleModel(Model):
    example_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    description = columns.Text(required=False)


class SampleModel(Model):
    p_type = columns.Text(primary_key= True)
    value = columns.Integer()

sync_table(ExampleModel)