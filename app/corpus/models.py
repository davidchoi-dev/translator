from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute


class Corpus():
    pass


class Translation(Model):
    class Meta:
        table_name = 'translation'

    timestamp = UTCDateTimeAttribute(range_key=True)
    raw = UnicodeAttribute()
    hash = UnicodeAttribute(hash_key=True)
    source_lang = UnicodeAttribute()
    target_lang = UnicodeAttribute()


if __name__ == '__main__':
    if not Translation.exists():
        Translation.create_table(read_capacity_units=1,
                                 write_capacity_units=1, wait=True)
