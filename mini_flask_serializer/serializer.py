from typing import List, Dict, Any, Set

from .exception import ValidationError


class MiniFlaskSerializer:
    """This mini_flask_serializer class is used to serializer an instance of your flask SQLAlchemy model.
    It return a json serialized format that you can use for your flask api."""

    def __init__(self):
        self.serialize = {} #An attribute that returns a JSON object.

    def serializer(self, obj: Any, exclude_fields: List[str] = None, include_fields: List[str] = None, many: bool = False, max_depth: int = 2, _current_depth: int = 0, _visited: Set[int] = None) -> Dict[str, Any]:
        
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

        if _visited is None:
            _visited = set()

        if many:
            if not hasattr(obj, "__iter__"):
                raise ValueError("Cannot serialize on many=True on non-iterable objects.")
            
            return [self._serializer(item, include_fields=include_fields, exclude_fields=exclude_fields, max_depth=max_depth, _current_depth=_current_depth, _visited=_visited) for item in obj]
        
        return self._serializer(obj, include_fields=include_fields, exclude_fields=exclude_fields, max_depth=max_depth, _visited=_visited, _current_depth=_current_depth)
    

    def _serializer(self, obj: Any, exclude_fields: List[str], include_fields: List[str], max_depth: int = 2, _current_depth: int = 0, _visited: Set[int] = None) -> Dict[str, Any]:

        if _visited is None:
            _visited - set()

        obj_id = id(obj)

        if obj_id in _visited:
            return {"CIRCULAR REFERENCE": True}
        
        _visited.add(obj_id)

        result = {}

        exclude_fields = exclude_fields or []
        include_fields = include_fields or []
        use_whitelist = len(include_fields) > 0

        if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict", None)):
            try:
                data: Dict[str, Any] = obj.to_dict()

                return self._filter_data(
                    data,
                    exclude_fields=exclude_fields,
                    include_fields=include_fields,
                    use_whitelist=use_whitelist,
                    max_depth=max_depth,
                    _current_depth=_current_depth,
                    _visited=_visited
                )
            except (AttributeError, TypeError):
                pass
        

        if hasattr(obj, "to_json") and callable(getattr(obj, "to_json", None)):
            try:
                data: Dict[str, Any] = obj.to_json()

                return self._filter_data(
                    data,
                    exclude_fields=exclude_fields,
                    include_fields=include_fields,
                    use_whitelist=use_whitelist,
                    max_depth=max_depth,
                    _current_depth=_current_depth,
                    _visited=_visited
                )
            except (AttributeError, TypeError):
                pass
    
        for attr in dir(obj):
            if attr.startswith("_") or callable(getattr(obj, attr)):
                continue
            if attr.startswith("query"):
                continue
            if attr.startswith("registry"):
                continue
            if attr.startswith("metadata"):
                continue
            if attr in exclude_fields:
                continue
            if use_whitelist and attr not in include_fields:
                continue

            value = getattr(obj, attr)

            if _current_depth < max_depth:
                result[attr] = self._serialize_value(
                    value,
                    exclude_fields=exclude_fields,
                    include_fields=include_fields,
                    max_depth=max_depth,
                    _current_depth=_current_depth,
                    _visited=_visited.copy()
                )
            else:
                result[attr] = self._serialize_simple_value(value)

        return result
    

    def _serialize_value(self, value: Any, exclude_fields: List[str], include_fields: List[str], max_depth: int, _current_depth: int, _visited: Set[int]) -> Any:
        if value is None:
            return None
        
        if isinstance(value, (str, int, float, bool)):
            return value
        
        if hasattr(value, "isoformat"):
            try:
                return value.isoformat()
            except:
                pass
        
        if hasattr(value, "__iter__") and not isinstance(value, (str, dict, bytes)):
            try:
                result = []

                for item in value:
                
                    if hasattr(item, "__tablename__") or hasattr(item, "_sa_instance_state"):

                        serialized = self._serializer(
                            item,
                            exclude_fields=exclude_fields,
                            include_fields=include_fields,
                            max_depth=max_depth,
                            _current_depth=_current_depth + 1,
                            _visited=_visited.copy()
                        )

                        result.append(serialized)

                    else:
                        serialized = self._serialize_value(
                            item,
                            exclude_fields=exclude_fields,
                            include_fields=include_fields,
                            max_depth=max_depth,
                            _current_depth=_current_depth + 1,
                            _visited=_visited.copy()
                        )
                        result.append(serialized)

                return result
                        
        
            except Exception as e:
                print("Error serializing list due to ", e)
                return self._serialize_simple_value(value)
            

        if isinstance(value, dict):
            return {
                k: self._serialize_value(
                        v,
                        exclude_fields=exclude_fields,
                        include_fields=include_fields,
                        max_depth=max_depth,
                        _current_depth=_current_depth + 1,
                        _visited=_visited.copy()
                    )
                    for k, v in value.items()
            }
        
        
        if hasattr(value, "__tablename__") or hasattr(value, "to_json") or hasattr(value, "to_dict") or hasattr(value, "_sa_instance_state"):
            return self._serializer(
                        value,
                        exclude_fields=exclude_fields,
                        include_fields=include_fields,
                        max_depth=max_depth,
                        _current_depth=_current_depth + 1,
                        _visited=_visited
                    )
        

        return self._serialize_simple_value(value)



    def _serialize_simple_value(self, value: Any) -> Any:

        if value is None:
            return None

        if isinstance(value, (str, float, int, bool)):
            return value

        
        if isinstance(value, bytes):
            try:
                return value.decode("utf-8")
            except:
                return str(value)

        try:
            from decimal import Decimal

            if isinstance(value, Decimal):
                return float(value)
        except ImportError:
            pass

        if hasattr(value, "_sa_instance_state"):
            if hasattr(value, "to_dict") and callable(getattr(value, "to_dict", None)):
                try:
                    return value.to_dict()
                except:
                    pass

        if hasattr(value, "__table__"):
            try:
                return {c.name: getattr(value, c.name) for c in value.__table__.columns}
            except:
                pass

        if hasattr(value, "__tablename__") or hasattr(value, "__dict__"):
            try:
                return {k: v for k, v in value.__dict__.items() if not k.startswith("_")}
            except:
                pass

        try:
            return str(value)
        except:
            return None     

    def _filter_data(self, data: Any, exclude_fields: List[str], include_fields: List[str], use_whitelist: bool, max_depth: int = 2, _current_depth: int = 0, _visited: Set[int] = None) -> Dict[str, Any]:
        """Helper methods to add exclude and include fields to to_dict and to_json method of the object model you want to serialize."""

        if _visited is None:
            _visited = set()

        result = {}

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

            if _current_depth < max_depth:
                result[key] = self._serialize_value(
                        value,
                        exclude_fields=exclude_fields,
                        include_fields=include_fields,
                        max_depth=max_depth,
                        _current_depth=_current_depth + 1,
                        _visited=_visited.copy()
                    )
            else:
                result[key] = self._serialize_simple_value(value)

        return result
    

    def validate_data(self, fields: Dict[str, Any], expected_fields: List[str] = False) -> Dict[str, Any]:
        """
            This functions does minimal validation on your api data and compares the fields your flask api is returning against your expected fields,
            to ensure you are getting the exact fields you want.

            Args:
                expepected_fields: default=False: A list of fields you are expecting from your api. e.g ["title", "content", "author"].
                fields: A dictionary gotten from your flask api that is suppose to match your expected_fields.

            Returns:
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
            
            if isinstance(value, str) and len(value) <= 2:
               raise ValidationError(f"{key} is too short.")
            
            
            self.serialize[key] = value

        return self.serialize


    def save_to_model(self, model_instance, model):
        """
            This function saves your request to the specified database only after it has been sanitized.

            Avoid this function if your data haven't been sanitized manually or automatically via the validate_date function.

            Args:
                model_instance: This represent the model in which you want to add data to. e.g User(), Note() class from your models.py or so.
                                Don't pass in with the () just User is ok.
                model: This represents your SQLAlchemy instance. e.g db = SQLAlcehmy(). The db or whatever name you use is what you will pass in.

            Returns:
                    An instance of model_instance.
                    
        """
        try:
            instance = model_instance()

            for key, value in self.serialize.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)

            if hasattr(model, "session"):
                model.session.add(instance)
                model.session.commit()
                
            self.serialize = {}
            
        except Exception as e:
            model.session.rollback()
            raise e
        
        return instance 