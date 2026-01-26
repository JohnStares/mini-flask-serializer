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


## [Version 2.1.0](https://github.com/JohnStares/mini-flask-serializer/tags) (2026-01-26)

### New Feature

- The clas MiniFlaskSerializer can now accept your flask app for the purpose of error handling: ['72c4ebd'](https://github.com/JohnStares/mini-flask-serializer/commit/72c4ebd796038b145796a46c053d514c367acd3d)

- Create error handler functions: ['52df215'](https://github.com/JohnStares/mini-flask-serializer/commit/52df215094c6306e777dc66ee5f59ad202da1120)

### Patches

- Raise errors rather than skipping them with the pass statement: ['8bdb7e9'](https://github.com/JohnStares/mini-flask-serializer/commit/8bdb7e9839783fc7b4bf68ee0cfb991fc455f553)

- Changed a type from - to =: ['260419b'](https://github.com/JohnStares/mini-flask-serializer/commit/260419b08000214f828d5764dca1bfdbb2dee029)
