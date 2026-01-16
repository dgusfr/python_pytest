# python-testes

Execução de testes unitario e de cobertura com arquivo pytest.ini:

```bash
pytest               
======================================== test session starts ========================================================
platform win32 -- Python 3.14.2, pytest-8.4.1, pluggy-1.6.0 -- C:\Projects\python_tests\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Projects\python_tests\burguer-app\auth-service
configfile: pytest.ini
plugins: cov-6.2.1
collected 5 items                                                                                                                                                             

test/test_user_model.py::test_complete_user PASSED                                                                                                                      [ 20%] 
test/test_user_model.py::test_user_string PASSED                                                                                                                        [ 40%] 
test/test_user_model.py::test_user_empty_dict PASSED                                                                                                                    [ 60%] 
test/test_user_model.py::test_user_missing_email PASSED                                                                                                                 [ 80%] 
test/test_user_model.py::test_user_dict_none PASSED                                                                                                                     [100%] 
ERROR: Coverage failure: total of 4 is less than fail-under=80


============================================= tests coverage =============================================== 
_______________________________________ coverage: platform win32, python 3.14.2-final-0 ________________________________ 

Name                             Stmts   Miss  Cover   Missing
--------------------------------------------------------------
config\__init__.py                   0      0   100%
config\database.py                   9      9     0%   5-23
controllers\__init__.py              0      0   100%
controllers\auth_controller.py      29     29     0%   1-37
models\user_model.py                 2      0   100%
services\__init__.py                 0      0   100%
services\auth_service.py            11     11     0%   4-26
--------------------------------------------------------------
TOTAL                               51     49     4%
FAIL Required test coverage of 80% not reached. Total coverage: 3.92%
=================================== 5 passed in 0.32s ============================================
```



## pylint 

Pip install pylint 

```bash
pylint .\config\
************* Module auth-service.config.database
config\database.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config\database.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
config\database.py:4:0: C0411: standard import "os" should be placed before third party import "pymongo.MongoClient" (wrong-import-order)

-----------------------------------
Your code has been rated at 6.25/10
```

```bash
pylint .\controllers\
************* Module auth-service.controllers.auth_controller
controllers\auth_controller.py:18:0: C0303: Trailing whitespace (trailing-whitespace)
controllers\auth_controller.py:1:0: C0114: Missing module docstring (missing-module-docstring)
controllers\auth_controller.py:2:0: E0401: Unable to import 'services.auth_service' (import-error)
controllers\auth_controller.py:3:0: E0401: Unable to import 'models.user_model' (import-error)
controllers\auth_controller.py:8:0: C0116: Missing function or method docstring (missing-function-docstring)
controllers\auth_controller.py:12:0: C0116: Missing function or method docstring (missing-function-docstring)
controllers\auth_controller.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
controllers\auth_controller.py:28:0: C0116: Missing function or method docstring (missing-function-docstring)
controllers\auth_controller.py:35:0: C0116: Missing function or method docstring (missing-function-docstring)

-----------------------------------
Your code has been rated at 2.92/10
```