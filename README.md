# Django LocationSpecificLocaleMiddleware

This title just can't be too long :) This middleware helps to create different parts of your site translated onto different language sets.

#Setup

Just download theses two files (middleware.py and utils.py), put in some app/project directory and change your default Django locale middleware with LocationSpecificLocaleMiddleware in your settings.py

Then configure location languages and fallbacks in your settings.py: 
```python
LOCATION_LANGUAGES = (
    # (('prefix', 'another_prefix'), ('lang1', 'lang2', 'lang3'), 'fallback_language')
    (('/translated_part_one/', '/translated_part_two/'), ('lv', 'et', 'lt', 'ru'), 'ru'),
    (('/translated_part_three/', '/translated_part_four/'), ('en', 'de', ), 'en'),
)
```
and just have fun!
