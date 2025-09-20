from typing import List, Dict, Any

from .exception import ValidationError


class MiniFlaskSerializer:
    """This mini_flask_serializer class is used to serializer an instance of your flask SQLAlchemy model.
    It return a json serialized format that you can use for your flask api."""

    def __init__(self):
        self.serialize = {} #An attribute that returns a JSON object.

    def serializer(self, obj: Any, exclude_fields: List[str] = None, include_fields: List[str] = None, many: bool = False) -> Dict[str, Any]:
        
        """
        Serialize an object with optional field filtering.
        
        Args:
            obj: Any object with attributes, to_dict(), or to_json() method
            exclude_fields: List of field names to exclude
            include_fields: List of field names to include (whitelist). This returns the fields name and values you specified in the include field.
            many: A boolean default to False for returning a single object of the model.
            
        Returns:
            Dictionary of serialized data
        """

        if many:
            if not hasattr(obj, "__iter__"):
                raise ValueError("Cannot serialize on many=True on non-iterable objects.")
            
            return [self._serializer(item, include_fields=include_fields, exclude_fields=exclude_fields) for item in obj]
        
        return self._serializer(obj, include_fields=include_fields, exclude_fields=exclude_fields)
    

    def _serializer(self, obj: Any, exclude_fields: List[str], include_fields: List[str]) -> Dict[str, Any]:

        self.serialize = {} # Repeated here to avoid accumulation of data.

        exclude_fields = exclude_fields or []
        include_fields = include_fields or []
        use_whitelist = len(include_fields) > 0

        if hasattr(obj, "to_dict"):
            data: Dict[str, Any] = obj.to_dict()

            return self._filter_data(data, exclude_fields=exclude_fields, include_fields=include_fields, use_whitelist=use_whitelist)

        if hasattr(obj, "to_json"):
            data: Dict[str, Any] = obj.to_json()

            return self._filter_data(data, exclude_fields=exclude_fields, include_fields=include_fields, use_whitelist=use_whitelist)



        for attr in dir(obj):
            if attr.startswith("_") or callable(getattr(obj, attr)):
                continue

            if attr.startswith("query"):
                continue

            if attr.startswith("metadata"):
                continue

            if attr.startswith("registry"):
                continue

            if attr in exclude_fields:
                continue

            if use_whitelist and attr not in include_fields:
                continue

            self.serialize[attr] = getattr(obj, attr)

        return self.serialize
    

    def _filter_data(self, data: Any, exclude_fields: List[str], include_fields: List[str], use_whitelist: bool) -> Dict[str, Any]:
        """Helper methods to add exclude and include fields to to_dict and to_json method of the object model you want to serialize."""

        self.serialize = {} # Repeated here to avoid accumulation of data.

        if isinstance(data, str):
            try:
                import json

                data: Dict[str, Any] = json.loads(data)
            except json.JSONDecodeError:
                return {}


        for key, value in data.items():
            if key in exclude_fields:
                continue

            if use_whitelist and key not in include_fields:
                continue

            self.serialize[key] = value

        return self.serialize
    

    def validate_data(self, fields: Dict[str, Any], expected_fields: List[str] = False) -> Dict[str, Any]:
        """
            This functions does minimal validation on your api data and compares the fields your flask api is returning against your expected fields,
            to ensure you are getting the exact fields you want.

            ARGS:
                expepected_fields: default=False: A list of fields you are expecting from your api. e.g ["title", "content", "author"].
                fields: A dictionary gotten from your flask api that is suppose to match your expected_fields.

            RETURNS:
                    A dictionary if all fields match or an error if it doesn't match.
        """
        self.serialize = {}

        if expected_fields:
            unexpected_fields = set(fields.keys()) - set(expected_fields)

            if unexpected_fields:
                raise ValidationError(f"{unexpected_fields} is not an expected field.")
            
            missing_fields = set(expected_fields) - set(fields.keys())
            
            if missing_fields:
                raise ValidationError(f"{missing_fields} field is required.")
  
        for key, value in fields.items():
            if key.startswith("_") or key.startswith("-") or key.startswith("/") or key.startswith("\\"):
                raise ValidationError(f"{key} cannot start with an underscore _ or hypen - or slash / or \\")
            
            if value == None or value == "" or value == " ":
                raise ValidationError(f"{key} can't be empty.")
            
            if len(value) <= 2:
               raise ValidationError(f"{key} is too short.")
            
            
            self.serialize[key] = value

        return self.serialize

