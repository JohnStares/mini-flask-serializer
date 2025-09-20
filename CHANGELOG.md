## [Version 0.1.1](https://github.com/JohnStares/mini-flask-serializer/tags) (2025-09-20)

### New Feature and Bug Fix

- Added many=True option and equally fixed a bug: ['156bc3e'](https://github.com/JohnStares/mini-flask-serializer/commit/34c41564c55106c64d3d43d81fdc4d8de5772863)


## [Version 1.0.0] (2025-09-20)

### New Feature 

- Added a validate_date method: It does minimal validation and compares your expected_fields agaisnt that returned by your api.
- Added a save_to_model method: It saves your post request data that you want to save directly to your database after validation.
- Addedd an exception.py file for handling exceptions.

### Patch

- Changed def serializer to def validate_data and added more note on the method documentation.
