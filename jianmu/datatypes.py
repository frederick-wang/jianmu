from typing import Dict, Sequence, Union

JSONValue = Union[str, int, float, bool, None, Dict[str, 'JSONValue'], Sequence['JSONValue']]
'''Type of the data that can be serialized to JSON.'''
