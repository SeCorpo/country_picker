# Country Picker

A small Python GUI application built with PyQt6 that fetches and displays country names from a public API.  

---

## Features

### Base Requirements
- GUI window with:
  - A `QComboBox` to display country names
  - A `QLabel` to show the selected country
- Fetches country data from `https://www.apicountries.com/countries`
- Parses JSON and extracts country names (data is parsed to list in country_picker_controller)
- Populates the combobox with names in **alphabetical order**, using locale for special characters
- When a country is selected, label shows `Selected: <country>`

### Bonus Objectives Implemented
- Runs JSON fetch and parsing in a background thread using `QThread`
- UI updates always happen in the main thread
- Supports pre-selecting a country from command line using:
  ```bash
  python -m country_picker --select Netherlands

### Tests (pytest)
- test_countries_is_list PASSED
- test_countries_not_empty PASSED
- test_all_countries_are_dicts PASSED
- test_first_country_has_name_key PASSED
- test_first_country_has_alpha2code_key PASSED
- test_first_country_has_region_key PASSED
- test_print_first_random_last_country_names PASSED

### Structure
```text
├── country_picker
│   ├── __main__.py
│   ├── core
│   │   ├── exceptions
│   │   ├── models
│   │   ├── service
│   │   │   └── fetch_countries_raw.py
│   │   └── utils
│   │       └── logger.py
│   ├── gui
│   │   ├── controllers
│   │   │   └── country_picker_controller.py
│   │   ├── threads
│   │   │   ├── country_fetch_thread.py
│   │   │   └── model_schema_thread.py
│   │   └── views
│   │       ├── country_picker_view.py
│   │       ├── defined_model_view.py
│   │       └── pydantic_dynamic_model_view.py
├── tests
│   └── test_fetch_countries_raw.py
├── README.md
├── requirements.txt
├── pytest.ini
```
---

### Please take a look at my other branches for:
- Dynamic schema generation — see the `interpretation` branch for runtime model construction based on API responses
- Defined model — see the `defined_model` branch for a manually curated and structured `Country` model using Pydantic
- Both branches have many tests
