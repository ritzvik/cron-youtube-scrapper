# Code Rules for Codr Service

## Entity Member functions

- All db methods(get, update, create) goes into entity member functions
- Structure is as:
- app_name
  - entity_member_functions
    - {model_name}_entity_member.py


## Model CRUD Interaction (Entity member function)

- to interact with any model for all read methods should be prefixed with `get_{}`
- to create any model object, methods should be prefixed with `create_{}`
- to update any model, methods should be prefixed with `update_{}`
- Sytem defaults should be prefixed with `get_default_{suffix}` for any **model entity** and should reside in same entity class



## Validation checks

All request data or query string validators goes into serialisers

- goes in serialiser, naming convention - {{api-class_name}_{?if method name}_serialiser.py} <https://www.django-rest-framework.org/api-guide/serializers/>
- serialisers can be improved as code matures

- app_name
  - api
    - serialisers
      - {{api-class_name}_{?if method name}_serialiser.py}